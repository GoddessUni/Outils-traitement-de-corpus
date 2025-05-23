import pandas as pd
import numpy as np
import re
import random
from sklearn.preprocessing import MultiLabelBinarizer
from nltk.corpus import wordnet
import nltk

nltk.download('wordnet')
nltk.download('omw-1.4')

CSV_PATH = "arxiv_abstracts_sampled100000.csv"  
OUTPUT_PATH = "augmented_data.csv"              
TEXT_FIELD = "abstract"
LABEL_FIELD = "categories"

# Enrichissement du corpus
def synonym_replacement(sentence, n=2):
    words = sentence.split()
    new_words = words.copy()
    random_word_list = list(set([word for word in words if len(word) > 3]))
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        synonyms = get_synonyms(random_word)
        if len(synonyms) >= 1:
            synonym = random.choice(list(synonyms))
            new_words = [synonym if word == random_word else word for word in new_words]
            num_replaced += 1
        if num_replaced >= n: 
            break
    return " ".join(new_words)

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name().replace('_', ' ').lower()
            if synonym != word.lower():
                synonyms.add(synonym)
    return synonyms

def preprocess_and_augment(df):
    def clean_text(text):
        text = str(text)
        text = text.replace("\n", " ").replace("\r", " ")
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def parse_labels(cat_str):
        try:
            cats = eval(cat_str)
            if isinstance(cats, list) and len(cats) > 0:
                all_cats = []
                for c in cats:
                    all_cats.extend(c.split())
                return list(set(all_cats))
            else:
                return []
        except:
            return []

    texts = []
    labels = []

    for _, row in df.iterrows():
        text = clean_text(row[TEXT_FIELD])
        label_list = parse_labels(row[LABEL_FIELD])
        if text and label_list:
            texts.append(text)
            labels.append(label_list)

    mlb = MultiLabelBinarizer()
    binary_labels = mlb.fit_transform(labels)
    classes = mlb.classes_

    augmented_texts = []
    augmented_labels = []

    for text, label_vec in zip(texts, binary_labels):
        augmented_texts.append(text)
        augmented_labels.append(label_vec)

        aug_text = synonym_replacement(text, n=2)
        if aug_text != text:
            augmented_texts.append(aug_text)
            augmented_labels.append(label_vec)

    print(f"Initial samples: {len(texts)}")
    print(f"Samples after augmentation: {len(augmented_texts)}")
    print(f"Categories: {len(classes)}")
    print(f"List of categories: {classes[:10]}")
    print(f"Texte sample:\n{augmented_texts[0]}")
    print(f"Label vector:\n{augmented_labels[0]}")

    return augmented_texts, augmented_labels, classes

def save_augmented_to_csv(texts, labels, classes, output_path=OUTPUT_PATH):
    label_strs = []
    for label_vec in labels:
        label_names = [classes[i] for i, v in enumerate(label_vec) if v == 1]
        label_strs.append(" ".join(label_names))

    df_out = pd.DataFrame({
        "text": texts,
        "labels": label_strs
    })
    df_out.to_csv(output_path, index=False)
    print(f"Données enregistré {output_path}")

def main():
    df = pd.read_csv(CSV_PATH)
    texts, labels, classes = preprocess_and_augment(df)
    save_augmented_to_csv(texts, labels, classes)

if __name__ == "__main__":
    main()
