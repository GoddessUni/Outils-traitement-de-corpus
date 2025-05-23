import pandas as pd

df = pd.read_csv("arxiv_abstracts_sampled100000.csv")

df_head = df.head(300)

df_head.to_csv("arxiv_abstracts_head300.csv", index=False)
