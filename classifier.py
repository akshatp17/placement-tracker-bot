from google import genai
from google.genai import types
import os
import time

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

PROMPT = """
You are filtering placement messages.

STORE if the message is:

- Internship
- Internship + FTE
- Full-time Job
- Placement Opportunity
- Recruitment Drive

STORE even if:

- Training is required before employment
- Service agreement exists
- Bond exists
- Internship duration is long

IGNORE:

- Webinars
- Career Guidance
- Courses
- Certifications
- OA Updates
- Interview Updates
- Results
- Shortlists
- Hackathons
- Competitions
- Learning Programs
- Women-only opportunities
- Standalone training programs that do not lead to employment

Return only:

STORE

or

IGNORE
"""


def classify_message(message: str):


    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{PROMPT}\n\nMESSAGE:\n{message}",
                config=types.GenerateContentConfig(
                    temperature=0
                )
            )

            result = response.text.strip().upper()

            if result not in ["STORE", "IGNORE"]:
                return "IGNORE"

            return result

        except Exception as e:

            error_text = str(e)

            if "429" in error_text:

                wait_time = 60

                print(f"\nRate limit hit. Waiting {wait_time}s...\n")

                time.sleep(wait_time)

                continue

            if "503" in error_text:

                print("\nGemini busy. Retrying...\n")

                time.sleep(10)

                continue

            print(f"\nGemini Error: {e}\n")

            return "IGNORE"

    return "IGNORE"