from telethon import TelegramClient
from telethon.sessions import StringSession

from config import (
    API_ID,
    API_HASH
)

with TelegramClient(
    StringSession(),
    API_ID,
    API_HASH
) as client:

    print("\nSESSION STRING:\n")
    print(client.session.save())