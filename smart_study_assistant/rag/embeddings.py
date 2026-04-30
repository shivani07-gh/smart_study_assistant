import faiss
import numpy as np
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 🔥 NVIDIA CLIENT
client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)

# 🔥 CREATE EMBEDDINGS (PASSAGE TYPE)
def create_embeddings(chunks):
    response = client.embeddings.create(
        input=chunks,
        model="nvidia/llama-3.2-nemoretriever-300m-embed-v1",
        extra_body={"input_type": "passage"}   # 🔥 VERY IMPORTANT
    )

    embeddings = [item.embedding for item in response.data]
    return embeddings


# 🔥 STORE IN FAISS
def store_in_faiss(embeddings):
    embeddings = np.array(embeddings).astype('float32')

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index