"""Admin-only /stats command: how many people have started the bot in a given
period, to gauge ad performance (e.g. Meta Ads -> bot starts) independent of how many
went on to register or pay. Reads the CSV written by start_log.py.
"""

import csv
import os
from collections import Counter
from datetime import datetime, timedelta, timezone

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from ..config import ADMIN_CHAT_ID
from ..start_log import LOG_FILE

# (label, how far back). Counts are as of "now" in UTC - PythonAnywhere's server
# clock - not the admin's local timezone.
_PERIODS = [
    ("Today (UTC)", timedelta(days=1)),
    ("Last 7 days", timedelta(days=7)),
    ("Last 30 days", timedelta(days=30)),
]


def _read_rows() -> list[dict]:
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, newline="") as f:
        return list(csv.DictReader(f))


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.effective_chat.id) != str(ADMIN_CHAT_ID):
        return

    rows = _read_rows()
    if not rows:
        await update.message.reply_text("No /start events logged yet.")
        return

    now = datetime.now(timezone.utc)
    lines = ["📊 *Bot starts*", ""]
    for label, span in _PERIODS:
        cutoff = now - span
        in_period = [r for r in rows if datetime.fromisoformat(r["timestamp"]) >= cutoff]
        unique = len({r["telegram_id"] for r in in_period})
        lines.append(f"{label}: {len(in_period)} starts, {unique} unique")

    total_unique = len({r["telegram_id"] for r in rows})
    lines.append("")
    lines.append(f"All-time: {len(rows)} starts, {total_unique} unique")

    # Breaks traffic down by /start deep-link tag, e.g. a Meta ad whose destination
    # is https://t.me/ezyregisterbot?start=metaad1 - lets Jack tell ad-driven starts
    # apart from organic ones without adding anything on the ad platform's side.
    tagged = Counter(r["tag"] for r in rows if r["tag"])
    if tagged:
        lines.append("")
        lines.append("By tag:")
        for tag, count in tagged.most_common():
            lines.append(f"  `{tag}`: {count}")

    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN)
