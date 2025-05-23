import os
"""
Finetuner le modèle pretrained qui correspond le plus à vos données grâce au trainer d’hugging face
"""

os.environ["TORCH_DISTRIBUTED_DEBUG"] = "DETAIL"

import torch

# Mon ordinateur n'a pas de GPU indépendante, donc je n'utilise que le CPU
def get_default_device():
    return torch.device("cpu")
torch.get_default_device = get_default_device

import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from sklearn.preprocessing import MultiLabelBinarizer
from datasets import Dataset
from sklearn.metrics import f1_score

AUG_DATA_PATH = "augmented_data.csv"
df = pd.read_csv(AUG_DATA_PATH)

# Convertir les multi-étiquettes à multi-hot vectors
df["labels_list"] = df["labels"].apply(lambda x: x.split())

mlb = MultiLabelBinarizer()
binary_labels = mlb.fit_transform(df["labels_list"])

dataset = Dataset.from_dict({
    "text": df["text"].tolist(),
    "labels": binary_labels.tolist()
})

MODEL_NAME = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Convertir les étiquettes à float
def format_and_cast_labels(examples):
    examples["labels"] = [list(map(float, label)) for label in examples["labels"]]
    return examples

tokenized_dataset = tokenized_dataset.map(format_and_cast_labels, batched=True)

# Convertir le dataset de Hugging Face à PyTorch Tensor
def transform(example):
    return {
        "input_ids": torch.tensor(example["input_ids"], dtype=torch.long),
        "attention_mask": torch.tensor(example["attention_mask"], dtype=torch.long),
        "labels": torch.tensor(example["labels"], dtype=torch.float),
    }

tokenized_dataset = tokenized_dataset.with_transform(transform)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(mlb.classes_),
    problem_type="multi_label_classification"
)

training_args = TrainingArguments(
    output_dir="./results",
    save_strategy="no",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=100,
    metric_for_best_model="f1",
)

# Evaluation: F-mesure
def compute_metrics(pred):
    logits, labels = pred
    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(torch.tensor(logits))
    y_pred = (probs >= 0.5).int().numpy()
    y_true = labels
    f1 = f1_score(y_true, y_pred, average="micro")
    return {"f1": f1}

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset,
    compute_metrics=compute_metrics,
)

trainer.train()

model.save_pretrained("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")
