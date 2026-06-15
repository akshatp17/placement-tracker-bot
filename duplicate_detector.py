import hashlib

seen_messages = set()

def is_duplicate(message: str):

    normalized = " ".join(
        message.lower().split()
    )

    digest = hashlib.md5(
        normalized.encode()
    ).hexdigest()

    if digest in seen_messages:
        return True

    seen_messages.add(digest)

    return False