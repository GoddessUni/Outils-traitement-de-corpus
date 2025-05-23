import pandas as pd
import random
import pickle

df = pd.read_csv("arxiv_abstracts_sampled100000.csv")

# Charger les étiquettes utilisé dans le corpus d'entrainement
with open("label_classes.pkl", "rb") as f:
    allowed_labels = set(pickle.load(f))

# Extraire des échantillons et filtrer les étiquettes
def clean_and_filter_labels(row):
    try:
        label_list = eval(row["categories"])
    except:
        return None  # Exclure les données qui ne peuvent pas être parsées
    filtered_labels = [label for label in label_list if label in allowed_labels]
    if not filtered_labels:
        return None
    return {
        "text": row["abstract"],
        "labels": " ".join(filtered_labels)
    }

# Essayer d'obtenir 100 échantillons 
valid_samples = []
attempts = 0
max_attempts = 10000

while len(valid_samples) < 100 and attempts < max_attempts:
    row = df.sample(n=1).iloc[0]
    result = clean_and_filter_labels(row)
    if result:
        valid_samples.append(result)
    attempts += 1

if len(valid_samples) < 100:
    print(f"On ne trouve que{len(valid_samples)} échantillons de test")
else:
    print("100 échantillons de test générés")

test_df = pd.DataFrame(valid_samples)
test_df.to_csv("test.csv", index=False)
