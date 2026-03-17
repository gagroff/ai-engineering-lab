import os
from openai import OpenAI

# Initialize client using API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("=== Prompt Lab (AI Enabled) ===")

while True:
    user_prompt = input("\nEnter a prompt (or type 'exit'): ")

    if user_prompt.lower() == "exit":
        print("Goodbye!")
        break

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )

        ai_response = response.choices[0].message.content

        print("\nAI Response:\n")
        print(ai_response)

    except Exception as e:
        print("\nError occurred:")
        print(e)