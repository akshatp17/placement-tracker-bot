from notion_client import Client
from dotenv import load_dotenv
import os
import json

load_dotenv()

notion = Client(
    auth=os.getenv("NOTION_TOKEN")
)

results = notion.search()

print(f"Found {len(results['results'])} objects\n")

for item in results["results"]:

    print("=" * 60)

    print("OBJECT:", item["object"])

    if "id" in item:
        print("ID:", item["id"])

    if item["object"] == "page":

        title = ""

        if "properties" in item:

            for prop in item["properties"].values():

                if prop["type"] == "title":

                    if prop["title"]:

                        title = prop["title"][0]["plain_text"]

        print("TITLE:", title)

    elif item["object"] == "database":

        print("DATABASE TITLE:",
              item["title"][0]["plain_text"]
              if item["title"] else "Untitled")