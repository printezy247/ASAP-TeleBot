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

# Optional - only needed for the Card/Bank/E-Wallet payment option (Telegram's native
# Payments, via a provider connected in @BotFather -> /mybots -> Payments -> e.g. iPay88).
# Leave blank until connected; that payment button will show a friendly "not available"
# message instead of erroring. Each connected provider gives its own token - only one can
# be "live" at a time here, since Telegram's sendInvoice takes a single provider_token.
# Swapping which connected provider is active is just changing this value, no code change.
TELEGRAM_PAYMENT_PROVIDER_TOKEN = os.environ.get("EZYMAP_TELEGRAM_PAYMENT_PROVIDER_TOKEN", "")

if not BOT_TOKEN:
    raise RuntimeError(
        "EZYMAP_BOT_TOKEN is not set. Add it to .env (see .env.example)."
    )
if not ADMIN_CHAT_ID:
    raise RuntimeError(
        "EZYMAP_ADMIN_CHAT_ID is not set. Add it to .env (see .env.example)."
    )
