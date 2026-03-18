import os
import json
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "prompt_log.json"

print("=== Prompt Lab (Logging Enabled) ===")

# Ensure log directory and file exist
LOG_DIR.mkdir(parents=True, exist_ok=True)
if not LOG_FILE.exists():
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)


def append_log(entry):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = json.load(f)

    logs.append(entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)

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

        # Create log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": user_prompt,
            "response": ai_response,
            "status": "success"
        }

        append_log(log_entry)

        print("\n[Saved to log]")

    except Exception as e:
        append_log({
            "timestamp": datetime.now().isoformat(),
            "prompt": user_prompt,
            "error": str(e),
            "status": "error"
        })
        print("\nError occurred:")
        print(e)