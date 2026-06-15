from google import genai
from google.genai import types

import os
import json
import time

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

PROMPT = """
Extract placement details from the message.

Return ONLY valid JSON.

{
  "company": "",
  "role": "",
  "stipend": "",
  "fte_package": "",
  "location": "",
  "opportunity_type": "",
  "duration": "",
  "bond": "",
  "bond_details": "",
  "ppo_conversion": "",
  "eligibility": "",
  "deadline": "",
  "application_link": ""
}

Rules:

company:
- Extract actual company name.
- Never return phrases like:
  "An exciting"
  "Direct"
  "FTE"
  "Internship"
  "Unknown Opportunity"

role:
- Extract role name.

opportunity_type:
- Internship
- Internship + FTE
- FTE
- Unknown

bond:
- Yes
- No
- Unknown

Return JSON only.
No markdown.
No explanation.
"""


def extract_gemini(message: str):

    for attempt in range(2):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{PROMPT}\n\nMESSAGE:\n{message}",
                config=types.GenerateContentConfig(
                    temperature=0
                )
            )

            text = response.text.strip()

            text = text.replace("```json", "")
            text = text.replace("```", "")

            return json.loads(text)

        except Exception as e:

            error_text = str(e)

            if "429" in error_text:

                print("Rate limited. Waiting 60s...")
                return None

            print(f"Extractor Error: {e}")

            break

    return {
        "company": "Unknown",
        "role": "Unknown",
        "stipend": "",
        "fte_package": "",
        "location": "",
        "opportunity_type": "Unknown",
        "duration": "",
        "bond": "Unknown",
        "bond_details": "",
        "ppo_conversion": "Unknown"
    }