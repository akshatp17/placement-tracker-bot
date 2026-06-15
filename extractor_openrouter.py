import requests
import os
import json
import re


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
- Never return:
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

ppo_conversion:
- Yes
- No
- Unknown

Return JSON only.
No markdown.
No explanation.
"""


def extract_openrouter(
    message: str,
    model: str
):

    try:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization":
                f"Bearer {os.getenv('OPENROUTER_API_KEY')}",

                "Content-Type":
                "application/json"
            },
            json={
                "model": model,

                "messages": [
                    {
                        "role": "user",
                        "content":
                        f"{PROMPT}\n\nMESSAGE:\n{message}"
                    }
                ],

                "temperature": 0
            },
            timeout=30
        )

        if response.status_code != 200:

            print(
                f"\nOpenRouter HTTP {response.status_code}"
            )

            print(
                response.text
            )

            return None

        data = response.json()

        text = (
            data["choices"][0]
            ["message"]["content"]
            .strip()
        )

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        # Fix trailing commas

        text = re.sub(
            r",\s*}",
            "}",
            text
        )

        text = re.sub(
            r",\s*]",
            "]",
            text
        )

        try:

            return json.loads(text)

        except json.JSONDecodeError:

            print(
                "\nJSON Decode Error"
            )

            print(
                "\nRAW RESPONSE:\n"
            )

            print(text)

            return None

    except Exception as e:

        print(
            f"OpenRouter Error ({model}):",
            e
        )

        return None