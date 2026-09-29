import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY)


def generate_workout_gemini(
    username,
    age,
    weight,
    goal,
    intensity
):
    prompt = f"""
Create a safe, beginner-friendly fitness plan for {username}.

Age: {age}
Weight: {weight}
Goal: {goal}
Intensity preference: {intensity}

Provide:
1. A simple weekly exercise schedule
2. Warm-up and cool-down guidance
3. General safety reminders
4. Rest and recovery guidance

Do not recommend extreme exercise, restrictive dieting, or unsafe activities.
Keep the plan appropriate for a teenager.

Use clear headings and simple language.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text