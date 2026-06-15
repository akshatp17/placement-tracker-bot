from notion_client import Client

from config import (
    NOTION_TOKEN,
    NOTION_DATABASE_ID
)

notion = Client(
    auth=NOTION_TOKEN
)


def job_exists(company, role):

    try:

        response = notion.data_sources.query(
            data_source_id=NOTION_DATABASE_ID
        )

        for page in response["results"]:

            properties = page["properties"]

            company_name = ""

            if properties["Company"]["title"]:
                company_name = (
                    properties["Company"]["title"][0]
                    ["plain_text"]
                )

            role_name = ""

            if properties["Role"]["rich_text"]:
                role_name = (
                    properties["Role"]["rich_text"][0]
                    ["plain_text"]
                )

            if (
                company_name.lower() == company.lower()
                and
                role_name.lower() == role.lower()
            ):
                return True

        return False

    except Exception as e:

        print("Duplicate Check Error:", e)

        return False