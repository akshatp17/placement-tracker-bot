# inspect_database.py
from notion_client import Client
from dotenv import load_dotenv
import os

load_dotenv()

notion = Client(
    auth=os.getenv("NOTION_TOKEN")
)

response = notion.data_sources.retrieve(
    data_source_id=os.getenv("NOTION_DATABASE_ID")
)

print(response)