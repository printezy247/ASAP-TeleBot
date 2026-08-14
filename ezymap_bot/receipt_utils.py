import uuid
from datetime import datetime, timezone


def generate_receipt_number() -> str:
    return f"EZY-{datetime.now(timezone.utc):%Y%m%d}-{uuid.uuid4().hex[:6].upper()}"
