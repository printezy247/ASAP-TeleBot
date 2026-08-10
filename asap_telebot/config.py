import os

from dotenv import load_dotenv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "")
PERSISTENCE_FILE = os.environ.get(
    "PERSISTENCE_FILE", os.path.join(PROJECT_ROOT, "bot_persistence.pickle")
)

# Only needed when running in webhook mode (see webhook_app.py). A random secret used as
# part of the webhook URL path so strangers can't POST fake updates to your bot.
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set. Copy .env.example to .env and fill in your bot token."
    )
if not ADMIN_CHAT_ID:
    raise RuntimeError(
        "ADMIN_CHAT_ID is not set. Copy .env.example to .env and fill in your admin chat id."
    )
