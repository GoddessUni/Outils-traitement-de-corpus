import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pickle

# Charger le modèle et tokenizer
model_path = "fine_tuned_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.eval()

# Charger la liste des étiquettes
with open("label_classes.pkl", "rb") as f:
    label_names = pickle.load(f)  # e.g. ['AI', 'math', 'quantum']

# lire le texte
txt_path = "en_wikipedia_org_wiki_Milky_Way_cleaned.txt"
with open(txt_path, "r", encoding="utf-8") as f:
    text = f.read().strip()

# Excodage du texte
inputs = tokenizer(
    text,
    padding=True,
    truncation=True,
    max_length=512,
    return_tensors="pt"
)

with torch.no_grad():
    outputs = model(**inputs)
    probs = torch.sigmoid(outputs.logits).squeeze().cpu().numpy()

# distribution des étiquettes
threshold = 0.3  
predicted_labels = [label for label, prob in zip(label_names, probs) if prob >= threshold]

print("échantillon du texte:\n", text[:200])
print("\ncatégories:")
print(predicted_labels)
print("\nprobabilité:")
for label, prob in zip(label_names, probs):
    print(f"{label}: {prob:.3f}")
