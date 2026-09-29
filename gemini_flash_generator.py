import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is missing. Please add it to the .env file."
    )

genai.configure(api_key=GOOGLE_API_KEY)


def generate_nutrition_tip_with_flash(goal):
    prompt = f"""
You are FitBuddy, an AI fitness assistant.

The user's fitness goal is:
{goal}

Give one concise and practical nutrition or recovery tip
that supports this goal.

Keep the answer easy to understand.

Examples of topics:
- protein
- hydration
- balanced meals
- recovery
- sleep
- post-workout nutrition

Do not provide medical diagnosis or treatment advice.
"""

    model = genai.GenerativeModel("gemini-3.8-flash")

    response = model.generate_content(prompt)

    return response.text