import pandas as pd


df = pd.read_json("data/intents.jsonl",lines=True)
df_train=df.sample(frac=0.995,random_state=200)
df_eval=df.drop(df_train.index)
df_train.to_json("data/ultrachat_chunk_train.jsonl", orient="records", lines=True)
df_eval.to_json("data/ultrachat_chunk_eval.jsonl", orient="records", lines=True)