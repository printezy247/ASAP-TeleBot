"""Append-only CSV log of every /start, independent of how many people go on to
register or pay - lets Jack answer "how many people started the bot in period X" to
gauge ad performance (e.g. Meta Ads -> bot starts), via the /stats admin command in
handlers/stats.py.
"""

import csv
import os
from datetime import datetime, timezone

from telegram import User

from .config import PROJECT_ROOT

LOG_FILE = os.path.join(PROJECT_ROOT, "data", "ezymap_starts.csv")
_FIELDS = ["timestamp", "telegram_id", "username", "first_name", "tag"]


def log_start(user: User, tag: str = "") -> None:
    """tag is the raw /start deep-link payload, if any (e.g. a Meta ad's
    ?start=<tag> destination URL) - lets /stats break traffic down by source.
    """
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    is_new = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=_FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "telegram_id": user.id,
                "username": user.username or "",
                "first_name": user.first_name or "",
                "tag": tag,
            }
        )
