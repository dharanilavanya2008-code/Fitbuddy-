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


def update_workout_plan(original_plan, feedback):
    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Here is the user's original 7-day workout plan:

---------------- ORIGINAL PLAN ----------------

{original_plan}

---------------- USER FEEDBACK ----------------

{feedback}

-------------------------------------------------

Create an updated 7-day workout plan.

Apply the user's feedback where it is reasonable.

Keep the plan structured from Day 1 through Day 7.

For each day include:
- Workout focus
- Warm-up
- Main workout
- Sets/repetitions or duration
- Rest
- Cooldown/recovery

Keep the plan practical and easy to understand.

Do not provide medical diagnosis or treatment advice.
"""

    model = genai.GenerativeModel("gemini-3.8-pro")

    response = model.generate_content(prompt)

    return response.text