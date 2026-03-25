import os
import json
from openai import OpenAI
from chunker import load_documents, chunk_documents_advanced

CACHE_FILE = "embeddings_cache.json"

# Build an OpenAI client using the API key from the environment.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_embedding(text):
    # Send one chunk of text to the embeddings API and return only the vector.
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def embed_chunks(chunks):
    # Preserve the original chunk metadata and attach an embedding to each one.
    embedded_chunks = []

    for chunk in chunks:
        # Each chunk is embedded independently so it can be searched later.
        embedding = generate_embedding(chunk["content"])

        embedded_chunks.append({
            "content": chunk["content"],
            "source": chunk["source"],
            "embedding": embedding
        })

    return embedded_chunks

def save_embeddings(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

def load_embeddings():
    if not os.path.exists(CACHE_FILE):
        return None

    with open(CACHE_FILE, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    cached = load_embeddings()

    if cached:
        print("Loaded embeddings from cache")
        embedded_chunks = cached
    else:
        print("Generating new embeddings...")

        docs = load_documents()
        chunks = chunk_documents_advanced(docs)

        embedded_chunks = embed_chunks(chunks)

        save_embeddings(embedded_chunks)
        print("Saved embeddings to cache")

    print(f"Total chunks: {len(embedded_chunks)}")