import requests
import os
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def create_embedding(text_list):
    # https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings
    r = requests.post("http://localhost:11434/api/embed",json={
        "model":"bge-m3",
        "input":text_list
    })

    embedding = r.json()['embeddings']
    return embedding

# a = create_embedding("Cat Sat On The Mat")
# print(a[0:5])

jsons = os.listdir("jsons")
my_dicts = []
chunk_id = 0

for json_file in jsons:
    with open (f"jsons/{json_file}") as f:
        contant = json.load(f)
    print(f"Creating Embeddings for {json_file}")
    embeddings = create_embedding([c["text"] for c in contant["chunks"]])

    for i,chunk in enumerate (contant["chunks"]):
        chunk['chunk_id'] = chunk_id
        chunk['embedding'] = embeddings[i]
        chunk_id+=1
        my_dicts.append(chunk)

# print(my_dicts)

df = pd.DataFrame.from_records(my_dicts)
print(df)

incoming_query = input("Ask A Question :")
question_embedding = create_embedding([incoming_query])[0]


#Find cosine_similarities of question_embeddings with other embeddings
# print(np.vstack(df['embedding'].values))
# print(np.vstack(df['embedding'].shape))
similarities = cosine_similarity(np.vstack(df['embedding']),[question_embedding]).flatten()
print(similarities)
top_results = 3
max_indx = similarities.argsort()[::-1][0:top_results]
print(max_indx)
new_df = df.loc[max_indx]
print(new_df[["title","number","text"]])