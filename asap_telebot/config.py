import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set. Copy .env.example to .env and fill in your bot token."
    )
if not ADMIN_CHAT_ID:
    raise RuntimeError(
        "ADMIN_CHAT_ID is not set. Copy .env.example to .env and fill in your admin chat id."
    )
