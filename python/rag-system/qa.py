import os
from openai import OpenAI

# Import your existing functions
from embedder import load_embeddings, generate_embedding
from search import vector_search

# Initialize OpenAI client using your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_context(chunks):
    """
    Combine retrieved chunks into a single context string.

    Why:
    The AI model needs relevant information to answer accurately.
    We provide it here.
    """
    context = ""

    for i, chunk in enumerate(chunks):
        context += f"\nSource {i+1} ({chunk['source']}):\n"
        context += chunk["content"] + "\n"

    return context


def ask_ai(question, context):
    """
    Send the question + context to the AI model.

    Why:
    This is what makes RAG powerful - the AI answers using YOUR data.
    """
    prompt = f"""
You are an AI assistant that answers questions using provided context.

Instructions:
- Use ONLY the information from the context below
- If the answer is not in the context, say "I don't know"
- Be clear and concise
- Cite sources when possible

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def main():
    print("=== Repository AI Assistant ===")

    # Load precomputed embeddings
    embedded_chunks = load_embeddings()

    while True:
        question = input("\nAsk a question (or type 'exit'): ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        # Step 1: Retrieve relevant chunks
        results = vector_search(question, embedded_chunks, top_k=3)

        # Step 2: Build context from results
        context = build_context(results)

        # Step 3: Ask AI using context
        answer = ask_ai(question, context)

        # Step 4: Print results
        print("\n=== Answer ===\n")
        print(answer)

        print("\n=== Sources ===")
        for r in results:
            print(f"- {r['source']} (score: {r['score']:.4f})")


if __name__ == "__main__":
    main()
import os
from openai import OpenAI

# Import your existing functions
from embedder import load_embeddings, generate_embedding
from search import vector_search

# Initialize OpenAI client using your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_context(chunks):
    """
    Combine retrieved chunks into a single context string.

    Why:
    The AI model needs relevant information to answer accurately.
    We provide it here.
    """
    context = ""

    for i, chunk in enumerate(chunks):
        context += f"\nSource {i+1} ({chunk['source']}):\n"
        context += chunk["content"] + "\n"

    return context


def ask_ai(question, context):
    """
    Send the question + context to the AI model.

    Why:
    This is what makes RAG powerful — the AI answers using YOUR data.
    """
    prompt = f"""
You are an AI assistant that answers questions using provided context.

Instructions:
- Use ONLY the information from the context below
- If the answer is not in the context, say "I don't know"
- Be clear and concise
- Cite sources when possible

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def main():
    print("=== Repository AI Assistant ===")

    # Load precomputed embeddings
    embedded_chunks = load_embeddings()

    while True:
        question = input("\nAsk a question (or type 'exit'): ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        # Step 1: Retrieve relevant chunks
        results = vector_search(question, embedded_chunks, top_k=3)

        # Step 2: Build context from results
        context = build_context(results)

        # Step 3: Ask AI using context
        answer = ask_ai(question, context)

        # Step 4: Print results
        print("\n=== Answer ===\n")
        print(answer)

        print("\n=== Sources ===")
        for r in results:
            print(f"- {r['source']} (score: {r['score']:.4f})")


if __name__ == "__main__":
    main()