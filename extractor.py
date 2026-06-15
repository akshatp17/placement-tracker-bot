import re


def extract_company(text):

    patterns = [

        r"([A-Za-z0-9&.\- ]+?)\s+Graduate Hiring Program",

        r"Campus Drive\s*[-–]\s*\*\*(.*?)\*\*",

        r"([A-Za-z0-9&.\- ]+?)\s+Internship Opportunity",

        r"([A-Za-z0-9&.\- ]+?)\s+Internship Recruitment",

        r"([A-Za-z0-9&.\- ]+?)\s+Recruitment",

        r"([A-Za-z0-9&.\- ]+?)\s+Hiring",

        r"About the Company:\s*(.*?)\s*\(",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            company = match.group(1)

            company = re.sub(
                r"[*_]+",
                "",
                company
            )

            return company.strip()

    return "Unknown"


def extract_role(text):

    role_patterns = [

        r"Job Role:\s*(.*)",

        r"Position:\s*(.*)",

        r"Role:\s*(.*)"
    ]

    for pattern in role_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1).strip()

    return "Unknown"