import numpy as np
import faiss
import pickle
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 🔥 NVIDIA CLIENT
client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)

# 🔥 GET QUERY EMBEDDING
def get_query_embedding(query):
    response = client.embeddings.create(
        input=[query],
        model="nvidia/llama-3.2-nemoretriever-300m-embed-v1",
        extra_body={"input_type": "query"}
    )

    return response.data[0].embedding   # ✅ VERY IMPORTANT


# 🔍 Search similar chunks
def search_similar_chunks(query, index, chunks, k=10):
    query_embedding = get_query_embedding(query)

    # ✅ FIX SHAPE
    query_embedding = np.array(query_embedding).astype('float32').reshape(1, -1)

    # ✅ CORRECT FAISS CALL
    distances, indices = index.search(query_embedding, k)

    results = [chunks[i] for i in indices[0] if i != -1]
    return results


# 💾 Save FAISS index
def save_index(index, path):
    faiss.write_index(index, path)


# 📂 Load FAISS index
def load_index(path):
    if not os.path.exists(path):
        raise FileNotFoundError("Index not found")
    return faiss.read_index(path)


# 💾 Save chunks
def save_chunks(chunks, path):
    with open(path, 'wb') as f:
        pickle.dump(chunks, f)


# 📂 Load chunks
def load_chunks(path):
    if not os.path.exists(path):
        raise FileNotFoundError("Chunks not found")
    with open(path, 'rb') as f:
        return pickle.load(f)