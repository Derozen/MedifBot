from mistralai import Mistral
import os
from dotenv import load_dotenv
load_dotenv()



client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

ultrachat_chunk_train = client.files.upload(file={
    "file_name": "ultrachat_chunk_train.jsonl",
    "content": open("data/ultrachat_chunk_train.jsonl", "rb"),
})
ultrachat_chunk_eval = client.files.upload(file={
    "file_name": "ultrachat_chunk_eval.jsonl",
    "content": open("data/ultrachat_chunk_eval.jsonl", "rb"),
})

print("Train file ID :", ultrachat_chunk_train.id)
print("Eval file ID  :", ultrachat_chunk_eval.id)

import time

created_jobs = client.fine_tuning.jobs.create(
    model="open-mistral-7b", 
    training_files=[{"file_id": ultrachat_chunk_train.id, "weight": 1}],
    validation_files=[ultrachat_chunk_eval.id], 
    hyperparameters={
        "training_steps": 10,
        "learning_rate":0.0001
    },
    auto_start=False
)
time.sleep(50)

client.fine_tuning.jobs.start(job_id = created_jobs.id)

print(created_jobs)

#You can go retrieve your Mistral api id on your account on : https://console.mistral.ai/build/finetuned-models