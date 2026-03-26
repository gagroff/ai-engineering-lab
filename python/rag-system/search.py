import math
import numpy as np
from embedder import load_embeddings, generate_embedding


def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


def search(query, embedded_chunks, top_k=3):
    query_embedding = generate_embedding(query)
    results = []

    for chunk in embedded_chunks:
        similarity = cosine_similarity(query_embedding, chunk["embedding"])
        results.append({
            "content": chunk["content"],
            "source": chunk["source"],
            "score": similarity,
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

def vector_search(query, embedded_chunks, top_k=3):
    # Turn the user's text query into an embedding vector, then wrap it in a
    # NumPy array so we can use fast vector math operations on it.
    query_embedding = np.array(generate_embedding(query))

    # Pull out just the embedding from each chunk and stack them into a single
    # 2D NumPy array. Each row represents one stored chunk embedding.
    embeddings = np.array([chunk["embedding"] for chunk in embedded_chunks])

    # Normalize the query and chunk vectors to length 1.
    # After normalization, a dot product is equivalent to cosine similarity,
    # which measures how closely two vectors point in the same direction.
    query_norm = query_embedding / np.linalg.norm(query_embedding)
    embeddings_norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    # Compute the similarity between the query vector and every chunk vector
    # in one operation. The result is a 1D array of similarity scores, where
    # each score corresponds to the chunk at the same index in embedded_chunks.
    similarities = np.dot(embeddings_norm, query_norm)

    # Sort the similarity scores by index, keep the last top_k entries
    # (the highest scores), then reverse them so the best result comes first.
    top_indices = similarities.argsort()[-top_k:][::-1]

    results = []

    for idx in top_indices:
        # Use the saved index to recover the original chunk metadata.
        chunk = embedded_chunks[idx]

        # Build the response object with the original text, its source, and
        # the similarity converted to a plain Python float for display/use.
        results.append({
            "content": chunk["content"],
            "source": chunk["source"],
            "score": float(similarities[idx])
        })

    # Return the top matching chunks in descending similarity order.
    return results

if __name__ == "__main__":
    # Load the previously saved chunks and their embeddings from disk so the
    # script can search over them without recomputing embeddings first.
    embedded_chunks = load_embeddings()

    # Ask the user for a natural-language question to search with.
    query = input("Enter your question: ")

    # Run the original search implementation so its output can be compared
    # against the NumPy-based vectorized search below.
    print("\n=== Simple Search ===")
    simple_results = search(query, embedded_chunks)

    for r in simple_results:
        print(f"{r['score']:.4f} | {r['source']}")

    # Run the vectorized search implementation, which does the same general
    # ranking job but uses NumPy operations over the full embedding matrix.
    print("\n=== Vector Search ===")
    vector_results = vector_search(query, embedded_chunks)

    for r in vector_results:
        print(f"{r['score']:.4f} | {r['source']}")