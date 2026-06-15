from extractor_ai import extract_gemini
from extractor_openrouter import extract_openrouter

from extractor import (
    extract_company,
    extract_role
)

BAD_COMPANIES = {
    "",
    "unknown",
    "direct",
    "hiring",
    "recruitment",
    "internship",
    "fte",
    "opportunity",
    "an exciting"
}


def is_valid(data):

    if not data:
        return False

    company = str(
        data.get(
            "company",
            ""
        )
    ).strip().lower()

    if company in BAD_COMPANIES:
        return False

    return True

def regex_fallback(message):

    return {
        "company": extract_company(message),

        "role": extract_role(message),

        "stipend": "",

        "fte_package": "",

        "location": "",

        "opportunity_type": "Unknown",

        "duration": "",

        "bond": "Unknown",

        "bond_details": "",

        "ppo_conversion": "Unknown",

        "eligibility": "",

        "deadline": "",

        "application_link": ""
    }


def extract_job(message):

    # Gemini

    result = extract_gemini(message)

    if is_valid(result):

        result.setdefault(
            "eligibility",
            ""
        )

        result.setdefault(
            "deadline",
            ""
        )

        result.setdefault(
            "application_link",
            ""
        )

        print(
            "✓ Gemini Extraction"
        )

        return result

    # DeepSeek

    result = extract_openrouter(
        message,
        "deepseek/deepseek-chat-v3-0324"
    )

    if is_valid(result):

        result.setdefault(
            "eligibility",
            ""
        )

        result.setdefault(
            "deadline",
            ""
        )

        result.setdefault(
            "application_link",
            ""
        )

        print(
            "✓ DeepSeek Extraction"
        )

        return result

    # Qwen

    result = extract_openrouter(
        message,
        "qwen/qwen3-32b:free"
    )

    if is_valid(result):

        result.setdefault(
            "eligibility",
            ""
        )

        result.setdefault(
            "deadline",
            ""
        )

        result.setdefault(
            "application_link",
            ""
        )

        print(
            "✓ Qwen Extraction"
        )

        return result

    print(
        "⚠ Using Regex Fallback"
    )

    return regex_fallback(
        message
    )