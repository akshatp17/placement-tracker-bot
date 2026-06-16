from telethon import TelegramClient
from telethon.sessions import StringSession

from config import (
    API_ID,
    API_HASH,
    GROUP_ID,
    TELEGRAM_SESSION
)

from filters import should_store
from duplicate_detector import is_duplicate

client = TelegramClient(
    StringSession(TELEGRAM_SESSION),
    API_ID,
    API_HASH
)


async def main():

    total = 0
    matched = 0
    ignored = 0

    async for msg in client.iter_messages(
        GROUP_ID,
        limit=10
    ):

        total += 1

        text = (msg.text or "").strip()

        if not text:
            continue

        if text.startswith("http") and len(text.split()) < 5:
            ignored += 1
            continue

        if is_duplicate(text):
            ignored += 1
            continue

        if should_store(text):

            matched += 1

            print("\n" + "=" * 100)
            print(f"🟡 FILTER MATCH #{matched}")
            print("=" * 100)

            print(text[:1000])

        else:

            ignored += 1

    print("\n")
    print("=" * 100)
    print("FILTER SUMMARY")
    print("=" * 100)

    print(f"Total Messages: {total}")
    print(f"Matched: {matched}")
    print(f"Ignored: {ignored}")


with client:
    client.loop.run_until_complete(main())