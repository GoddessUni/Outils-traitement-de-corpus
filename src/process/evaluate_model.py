import pandas as pd
import numpy as np
import torch
import pickle
from sklearn.metrics import classification_report, hamming_loss, accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import MultiLabelBinarizer
from torch.utils.data import DataLoader, TensorDataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def evaluate_multilabel(y_true, y_pred_probs, label_names, threshold=0.5):
    # Résultats de prédiction binaire
    y_pred = (y_pred_probs >= threshold).astype(int)

    print(f"\n=== Threshold: {threshold:.2f} ===")
    print("Hamming Loss:", hamming_loss(y_true, y_pred))
    print("Accuracy (exact match):", accuracy_score(y_true, y_pred))
    print("Micro Precision:", precision_score(y_true, y_pred, average='micro', zero_division=0))
    print("Micro Recall:", recall_score(y_true, y_pred, average='micro', zero_division=0))
    print("Micro F1:", f1_score(y_true, y_pred, average='micro', zero_division=0))
    print("\nClassification Report:\n")
    print(classification_report(y_true, y_pred, target_names=label_names, zero_division=0))

def main():
    # Charger les classes des étiquette
    with open("label_classes.pkl", "rb") as f:
        label_names = pickle.load(f)

    df = pd.read_csv("test.csv")
    df = df.dropna(subset=["text"])
    df["label_list"] = df["labels"].apply(lambda x: x.strip().split(" "))

    # Convertir les étiquettes en binaires
    mlb = MultiLabelBinarizer(classes=label_names)
    y_true = mlb.fit_transform(df["label_list"])
    texts = df["text"].tolist()

    # Charger le modèle et tokenizer
    model_path = "fine_tuned_model"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Encodage du texte
    encodings = tokenizer(texts, truncation=True, padding=True, return_tensors='pt')
    input_ids = encodings["input_ids"]
    attention_mask = encodings["attention_mask"]

    dataset = TensorDataset(input_ids, attention_mask)
    loader = DataLoader(dataset, batch_size=16)

    # Prédiction
    all_probs = []
    with torch.no_grad():
        for batch in loader:
            b_input_ids, b_attention_mask = [b.to(device) for b in batch]
            outputs = model(b_input_ids, attention_mask=b_attention_mask)
            logits = outputs.logits
            probs = torch.sigmoid(logits).cpu().numpy()
            all_probs.append(probs)

    y_pred_probs = np.vstack(all_probs)

    # Évaluation
    for threshold in [0.3, 0.4, 0.5, 0.6]:
        evaluate_multilabel(y_true, y_pred_probs, label_names, threshold)

if __name__ == "__main__":
    main()
