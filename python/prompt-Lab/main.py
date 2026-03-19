import os
import json
from datetime import datetime
from pathlib import Path
from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError

MODEL = "gpt-4o-mini"
EXIT_COMMAND = "exit"

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "prompt_log.json"


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable is not set.")
    return OpenAI(api_key=api_key)


def setup_log() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def append_log(entry: dict) -> None:
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        logs = []

    logs.append(entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)


def call_api(client: OpenAI, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_prompt}]
    )
    return response.choices[0].message.content


def handle_prompt(client: OpenAI, user_prompt: str) -> None:
    try:
        ai_response = call_api(client, user_prompt)
        print(f"\nAI Response:\n\n{ai_response}")
        append_log({
            "timestamp": datetime.now().isoformat(),
            "prompt": user_prompt,
            "response": ai_response,
            "status": "success",
        })
        print("\n[Saved to log]")

    except AuthenticationError:
        print("\nError: Invalid API key. Check your OPENAI_API_KEY.")
        append_log({"timestamp": datetime.now().isoformat(), "prompt": user_prompt, "error": "AuthenticationError", "status": "error"})

    except RateLimitError:
        print("\nError: Rate limit reached. Please wait before retrying.")
        append_log({"timestamp": datetime.now().isoformat(), "prompt": user_prompt, "error": "RateLimitError", "status": "error"})

    except APIConnectionError:
        print("\nError: Could not connect to the API. Check your internet connection.")
        append_log({"timestamp": datetime.now().isoformat(), "prompt": user_prompt, "error": "APIConnectionError", "status": "error"})

    except Exception as e:
        print(f"\nUnexpected error: {e}")
        append_log({"timestamp": datetime.now().isoformat(), "prompt": user_prompt, "error": str(e), "status": "error"})


def run_prompt_loop(client: OpenAI) -> None:
    while True:
        user_prompt = input(f"\nEnter a prompt (or type '{EXIT_COMMAND}'): ").strip()

        if not user_prompt:
            continue

        if user_prompt.lower() == EXIT_COMMAND:
            print("Goodbye!")
            break

        handle_prompt(client, user_prompt)


def main() -> None:
    print("=== Prompt Lab (Logging Enabled) ===")
    setup_log()
    client = get_client()
    run_prompt_loop(client)


if __name__ == "__main__":
    main()
