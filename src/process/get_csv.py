import pandas as pd
from datasets import load_dataset # !pip install datasets

# Load dataset
dataset = load_dataset("gfissore/arxiv-abstracts-2021", split="train")
df = pd.DataFrame(dataset)

# Sample 10,000 rows to reduce size
df_sampled = df.sample(n=100000, random_state=42)

# Save to CSV
df_sampled.to_csv("arxiv_abstracts_sampled100000.csv", index=False)
print("Dataset saved as arxiv_abstracts_sampled.csv")