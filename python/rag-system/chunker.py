import os

KNOWLEDGE_PATH = "../../knowledge"


def load_documents():
    documents = []

    for filename in os.listdir(KNOWLEDGE_PATH):
        file_path = os.path.join(KNOWLEDGE_PATH, filename)

        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

                documents.append({
                    "content": content,
                    "source": filename
                })

    return documents

def simple_chunk(text, chunk_size=300):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks

def chunk_documents_simple(documents):
    all_chunks = []

    for doc in documents:
        chunks = simple_chunk(doc["content"])

        for chunk in chunks:
            all_chunks.append({
                "content": chunk,
                "source": doc["source"]
            })

    return all_chunks

def advanced_chunk(text, chunk_size=300):
    sentences = text.split(".")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        # Add sentence to current chunk
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def chunk_documents_advanced(documents):
    all_chunks = []

    for doc in documents:
        chunks = advanced_chunk(doc["content"])

        for chunk in chunks:
            all_chunks.append({
                "content": chunk,
                "source": doc["source"]
            })

    return all_chunks

if __name__ == "__main__":
    docs = load_documents()

    print("=== SIMPLE CHUNKING ===")
    simple_chunks = chunk_documents_simple(docs)
    print(f"Chunks: {len(simple_chunks)}\n")

    print("=== ADVANCED CHUNKING ===")
    advanced_chunks = chunk_documents_advanced(docs)
    print(f"Chunks: {len(advanced_chunks)}\n")

    for c in advanced_chunks[:3]:
        print(f"Source: {c['source']}")
        print(f"Chunk: {c['content']}\n")