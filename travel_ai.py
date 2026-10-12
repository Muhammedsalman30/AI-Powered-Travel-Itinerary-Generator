import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Find project directory
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables
env_path = BASE_DIR / ".env"

load_dotenv(dotenv_path=env_path, override=True)

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        f"Gemini API key not found. Check: {env_path}"
    )

# Connect to Gemini
client = genai.Client(api_key=api_key)


# Generate travel itinerary
def generate_itinerary(destination, days, budget, interests):

    prompt = f"""
    You are a professional travel assistant
    working for a travel company.

    Create a {days}-day travel itinerary.

    Destination: {destination}
    Budget: {budget}
    Interests: {interests}

    For each day include:

    1. Morning activities
    2. Afternoon activities
    3. Evening activities

    Also include:
    - Recommended attractions
    - Food recommendations
    - Local transportation suggestions
    - Travel tips

    Requirements:
    - Use professional language.
    - Organize the itinerary day by day.
    - Do not invent confirmed bookings.
    - Do not invent current prices or availability.
    - Mention that all travel information requires verification.
    """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    return response.text