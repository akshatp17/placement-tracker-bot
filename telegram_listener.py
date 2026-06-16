from telethon import TelegramClient, events
from telethon.sessions import StringSession

from config import (
    API_ID,
    API_HASH,
    GROUP_ID,
    TELEGRAM_SESSION
)

from filters import should_store
from extractor import (
    extract_company,
    extract_role
)

from notion_service import create_job_entry
from notion_duplicate import job_exists

from job_extractor import extract_job

client = TelegramClient(
    StringSession(TELEGRAM_SESSION),
    API_ID,
    API_HASH
)


@client.on(events.NewMessage(chats=GROUP_ID))
async def handler(event):

    try:

        text = (event.raw_text or "").strip()

        if not text:
            return

        if not should_store(text):
            return

        job = extract_job(text)

        company = job["company"]
        role = job["role"]

        print("\nMATCH FOUND")
        print("Company:", company)
        print("Role:", role)

        if job_exists(company, role):

            print("⚠️ Duplicate Found")
            return

        create_job_entry(
            job,
            text,
            event.id,
            event.date
        )

        print("✅ Saved To Notion")

    except Exception as e:

        print(
            f"Listener Error: {e}"
        )

def start_listener():

    print("Listening for placement opportunities...")

    client.start()

    client.run_until_disconnected()