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

# Optional - only needed for the Xendit (card/bank/e-wallet) payment option. Leave blank
# until you've signed up with Xendit; that payment button will show a friendly "not set
# up yet" message instead of erroring.
XENDIT_SECRET_KEY = os.environ.get("EZYMAP_XENDIT_SECRET_KEY", "")
# The "Verification Token" Xendit shows you when you set up a webhook callback in their
# dashboard. Used to confirm incoming webhook calls really came from Xendit.
XENDIT_CALLBACK_TOKEN = os.environ.get("EZYMAP_XENDIT_CALLBACK_TOKEN", "")
INVOICE_STORE_FILE = os.environ.get(
    "EZYMAP_INVOICE_STORE_FILE", os.path.join(PROJECT_ROOT, "ezymap_xendit_invoices.json")
)

if not BOT_TOKEN:
    raise RuntimeError(
        "EZYMAP_BOT_TOKEN is not set. Add it to .env (see .env.example)."
    )
if not ADMIN_CHAT_ID:
    raise RuntimeError(
        "EZYMAP_ADMIN_CHAT_ID is not set. Add it to .env (see .env.example)."
    )
