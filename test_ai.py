from telethon import TelegramClient
import time
from telethon.sessions import StringSession

from config import (
    API_ID,
    API_HASH,
    GROUP_ID,
    TELEGRAM_SESSION
)

from filters import should_store
from classifier import classify_message

client = TelegramClient(
    StringSession(TELEGRAM_SESSION),
    API_ID,
    API_HASH
)


async def main():

    total = 0
    keyword_matches = 0
    keyword_ignored = 0

    ai_store = 0
    ai_ignore = 0

    seen_messages = set()

    print("\nTesting last 100 messages...\n")

    async for msg in client.iter_messages(
        GROUP_ID,
        limit=40
    ):

        total += 1

        text = (msg.text or "").strip()

        if not text:
            continue

        # Skip duplicates
        message_hash = hash(text)

        if message_hash in seen_messages:
            continue

        seen_messages.add(message_hash)

        # Stage 1 - Keyword Filter
        if not should_store(text):

            keyword_ignored += 1

            print("\n" + "=" * 100)
            print(f"❌ FILTER IGNORED #{keyword_ignored}")
            print("-" * 100)
            print(text[:300])

            continue

        keyword_matches += 1

        print("\n" + "=" * 100)
        print(f"🟡 FILTER MATCH #{keyword_matches}")
        print("=" * 100)

        print(text[:1000])

        # Stage 2 - Gemini

        decision = classify_message(text)

        print("\nAI DECISION:", decision)

        if decision == "STORE":

            ai_store += 1

            print("✅ FINAL STORE")

        else:

            ai_ignore += 1

            print("❌ FINAL IGNORE")

        # Prevent Gemini RPM limit
        time.sleep(12)

    print("\n")
    print("=" * 100)
    print("FINAL SUMMARY")
    print("=" * 100)

    print(f"Total Messages: {total}")

    print("\nKeyword Filter")
    print(f"Matched: {keyword_matches}")
    print(f"Ignored: {keyword_ignored}")

    print("\nGemini")
    print(f"STORE: {ai_store}")
    print(f"IGNORE: {ai_ignore}")

    print("\nFinal Opportunities:")
    print(ai_store)


with client:
    client.loop.run_until_complete(main())