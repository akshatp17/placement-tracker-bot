from telethon import TelegramClient

from config import (
    API_ID,
    API_HASH,
    GROUP_ID
)

from filters import should_store

from job_extractor import extract_job

from notion_service import create_job_entry
from notion_duplicate import job_exists


client = TelegramClient(
    "placement_session",
    API_ID,
    API_HASH
)


async def main():

    added = 0
    scanned = 0

    async for msg in client.iter_messages(
        GROUP_ID,
        limit=500
    ):

        scanned += 1

        text = (msg.text or "").strip()

        if not text:
            continue

        if not should_store(text):
            continue

        print("\n" + "=" * 120)
        print(f"MATCH #{added + 1}")
        print("=" * 120)

        try:

            job = extract_job(text)

            company = job.get(
                "company",
                "unknown"
            )

            role = job.get(
                "role",
                "unknown"
            )

            print("\nEXTRACTED JSON")
            print("-" * 120)

            for key, value in job.items():
                print(f"{key}: {value}")

            if job_exists(
                company,
                role
            ):

                print(
                    "\n⚠ Duplicate Found"
                )

                continue

            create_job_entry(
                job,
                text,
                msg.id,
                msg.date
            )

            added += 1

            print(
                f"\n✅ Added #{added}: "
                f"{company}"
            )

        except Exception as e:

            print(
                f"\n❌ ERROR: {e}"
            )

            print(
                "\nOriginal Message:"
            )

            print(
                text[:1500]
            )

            continue

    print("\n" + "=" * 120)
    print("FINAL SUMMARY")
    print("=" * 120)

    print(
        f"Messages Scanned: {scanned}"
    )

    print(
        f"Opportunities Added: {added}"
    )


with client:
    client.loop.run_until_complete(main())