from notion_client import Client
import os
from dotenv import load_dotenv

load_dotenv()

notion = Client(
    auth=os.getenv("NOTION_TOKEN")
)

response = notion.databases.retrieve(
    database_id=os.getenv("NOTION_DATABASE_ID")
)

print(response["title"])