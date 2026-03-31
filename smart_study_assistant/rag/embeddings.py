from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# model load (only once)
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(chunks):
    embeddings = model.encode(chunks)
    return np.array(embeddings)

def store_in_faiss(embeddings):
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index