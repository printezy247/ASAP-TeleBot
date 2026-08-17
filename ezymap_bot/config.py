import os

from dotenv import load_dotenv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

BOT_TOKEN = os.environ.get("EZYMAP_BOT_TOKEN", "")
ADMIN_CHAT_ID = os.environ.get("EZYMAP_ADMIN_CHAT_ID", "")
PERSISTENCE_FILE = os.environ.get(
    "EZYMAP_PERSISTENCE_FILE", os.path.join(PROJECT_ROOT, "ezymap_bot_persistence.pickle")
)

# Only needed when running in webhook mode (see webhook_app.py). A random secret used as
# part of the webhook URL path so strangers can't POST fake updates to your bot.
WEBHOOK_SECRET = os.environ.get("EZYMAP_WEBHOOK_SECRET", "")

if not BOT_TOKEN:
    raise RuntimeError(
        "EZYMAP_BOT_TOKEN is not set. Add it to .env (see .env.example)."
    )
if not ADMIN_CHAT_ID:
    raise RuntimeError(
        "EZYMAP_ADMIN_CHAT_ID is not set. Add it to .env (see .env.example)."
    )
