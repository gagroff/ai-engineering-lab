import os

KNOWLEDGE_PATH = "../../knowledge"


def load_documents():
    documents = []

    # Loop through all files in the knowledge folder
    for filename in os.listdir(KNOWLEDGE_PATH):
        file_path = os.path.join(KNOWLEDGE_PATH, filename)

        # Only process files (skip folders)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

                documents.append({
                    "content": content,
                    "source": filename
                })

    return documents


if __name__ == "__main__":
    docs = load_documents()

    print(f"Loaded {len(docs)} documents:\n")

    for doc in docs:
        print(f"Source: {doc['source']}")
        print(f"Preview: {doc['content'][:100]}...\n")