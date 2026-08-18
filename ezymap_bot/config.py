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

# NOWPayments (card/e-wallet checkout that settles as USDT) - all optional. If
# NOWPAYMENTS_API_KEY is unset, the "Pay by Card" button tells the client that payment
# method is unavailable right now instead of erroring, same pattern as the old Xendit
# integration.
NOWPAYMENTS_API_KEY = os.environ.get("NOWPAYMENTS_API_KEY", "")
NOWPAYMENTS_IPN_SECRET = os.environ.get("NOWPAYMENTS_IPN_SECRET", "")
NOWPAYMENTS_INVOICE_STORE_FILE = os.environ.get(
    "NOWPAYMENTS_INVOICE_STORE_FILE", os.path.join(PROJECT_ROOT, "ezymap_nowpayments_invoices.json")
)
# Your bot's own public HTTPS base URL (e.g. https://<user>.pythonanywhere.com), no
# trailing slash. NOWPayments needs this to know where to POST payment confirmations -
# unlike Telegram, which calls a URL you gave *it* once via setWebhook, NOWPayments
# needs a fresh callback URL on every invoice we create.
EZYMAP_PUBLIC_BASE_URL = os.environ.get("EZYMAP_PUBLIC_BASE_URL", "").rstrip("/")

if not BOT_TOKEN:
    raise RuntimeError(
        "EZYMAP_BOT_TOKEN is not set. Add it to .env (see .env.example)."
    )
if not ADMIN_CHAT_ID:
    raise RuntimeError(
        "EZYMAP_ADMIN_CHAT_ID is not set. Add it to .env (see .env.example)."
    )
