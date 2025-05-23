import pandas as pd
import pickle
from sklearn.preprocessing import MultiLabelBinarizer

df = pd.read_csv("augmented_data.csv")
df["labels_list"] = df["labels"].apply(lambda x: x.split())

mlb = MultiLabelBinarizer()
mlb.fit(df["labels_list"])

with open("label_classes.pkl", "wb") as f:
    pickle.dump(mlb.classes_, f)

print("label_classes.pkl saved with", len(mlb.classes_), "classes.")