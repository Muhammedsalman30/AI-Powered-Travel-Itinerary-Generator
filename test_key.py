import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load .env file
env_path = Path(__file__).with_name(".env")

load_dotenv(dotenv_path=env_path, override=True)

# Read API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("ERROR: Gemini API key not found!")

else:
    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents="Write a welcome message for a travel company."
        )

        print("SUCCESS: Gemini API connected!")
        print("\nAI Response:")
        print(response.text)

    except Exception as e:
        print("Gemini connection failed:")
        print(e)