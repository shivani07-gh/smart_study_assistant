import numpy as np
import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')


# 🔍 Search similar chunks
def search_similar_chunks(query, index, chunks, k=3):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)

    results = [chunks[i] for i in indices[0]]
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