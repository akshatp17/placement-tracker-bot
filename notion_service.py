from notion_client import Client
from dateutil import parser
import re

from config import (
    NOTION_TOKEN,
    NOTION_DATABASE_ID
)

notion = Client(
    auth=NOTION_TOKEN
)


def parse_date(date_text):

    if not date_text:
        return None

    try:
        return parser.parse(
            date_text,
            fuzzy=True
        ).date().isoformat()

    except Exception:
        return None


def extract_application_link(message):

    urls = re.findall(
        r"https?://[^\s*]+",
        message
    )

    if urls:
        return urls[-1]

    return None


def create_job_entry(
    job,
    original_message
):

    deadline = parse_date(
        job.get("deadline", "")
    )

    application_link = extract_application_link(
        original_message
    )

    # -----------------------------
    # Normalize Notion Select Fields
    # -----------------------------

    opportunity_type = str(
        job.get(
            "opportunity_type",
            "Unknown"
        )
    ).strip()

    if opportunity_type not in [
        "Internship",
        "Internship + FTE",
        "FTE",
        "Unknown"
    ]:
        opportunity_type = "Unknown"

    bond = str(
        job.get(
            "bond",
            "Unknown"
        )
    ).strip()

    if bond not in [
        "Yes",
        "No",
        "Unknown"
    ]:
        bond = "Unknown"

    ppo_conversion = str(
        job.get(
            "ppo_conversion",
            "Unknown"
        )
    ).strip()

    if ppo_conversion not in [
        "Yes",
        "No",
        "Unknown"
    ]:
        ppo_conversion = "Unknown"

    properties = {

        "Company": {
            "title": [
                {
                    "text": {
                        "content":
                        str(
                            job.get(
                                "company",
                                "Unknown"
                            )
                        )
                    }
                }
            ]
        },

        "Status": {
            "status": {
                "name": "Unknown"
            }
        },

        "Platform": {
            "select": {
                "name": "Telegram"
            }
        },

        "On Campus / Off Campus": {
            "select": {
                "name": "On Campus"
            }
        },

        "Role": {
            "rich_text": [
                {
                    "text": {
                        "content":
                        str(
                            job.get(
                                "role",
                                ""
                            )
                        )
                    }
                }
            ]
        },

        "Location": {
            "rich_text": [
                {
                    "text": {
                        "content":
                        str(
                            job.get(
                                "location",
                                ""
                            )
                        )
                    }
                }
            ]
        },

        "Stipend": {
            "rich_text": [
                {
                    "text": {
                        "content":
                        str(
                            job.get(
                                "stipend",
                                ""
                            )
                        )
                    }
                }
            ]
        },

        "FTE Package": {
            "rich_text": [
                {
                    "text": {
                        "content":
                        str(
                            job.get(
                                "fte_package",
                                ""
                            )
                        )
                    }
                }
            ]
        },

        "Duration": {
            "rich_text": [
                {
                    "text": {
                        "content":
                        str(
                            job.get(
                                "duration",
                                ""
                            )
                        )
                    }
                }
            ]
        },

        "Eligibility": {
            "rich_text": [
                {
                    "text": {
                        "content":
                        str(
                            job.get(
                                "eligibility",
                                ""
                            )
                        )
                    }
                }
            ]
        },

        "Bond Details": {
            "rich_text": [
                {
                    "text": {
                        "content":
                        str(
                            job.get(
                                "bond_details",
                                ""
                            )
                        )
                    }
                }
            ]
        },

        "Opportunity Type": {
            "select": {
                "name": opportunity_type
            }
        },

        "Bond": {
            "select": {
                "name": bond
            }
        },

        "PPO Conversion": {
            "select": {
                "name": ppo_conversion
            }
        },

        "Priority": {
            "select": {
                "name": "Medium"
            }
        },

        "Original Message": {
            "rich_text": [
                {
                    "text": {
                        "content":
                        original_message[:1800]
                    }
                }
            ]
        }
    }

    if application_link:

        properties[
            "Application Link"
        ] = {
            "url": application_link
        }

    if deadline:

        properties[
            "Deadline"
        ] = {
            "date": {
                "start": deadline
            }
        }

    notion.pages.create(

        parent={
            "data_source_id":
            NOTION_DATABASE_ID
        },

        properties=properties
    )

    print(
        f"✅ Added: "
        f"{job.get('company', 'Unknown')}"
    )