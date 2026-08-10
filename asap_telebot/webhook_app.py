"""Webhook entry point for free always-on hosts (e.g. PythonAnywhere) that run a
single long-lived WSGI process but don't allow a background polling loop.

Telegram POSTs each update to /webhook/<WEBHOOK_SECRET>. We rebuild the
Application per request (loading its state from PERSISTENCE_FILE) so this
works correctly regardless of how many worker processes the host uses.
"""

import asyncio
import logging

from flask import Flask, abort, request
from telegram import Update

from .config import WEBHOOK_SECRET
from .main import build_application

if not WEBHOOK_SECRET:
    raise RuntimeError(
        "WEBHOOK_SECRET is not set. Add a random string to your .env, e.g. "
        "WEBHOOK_SECRET=some-long-random-string"
    )

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

app = Flask(__name__)


async def _process_update(update_data: dict) -> None:
    application = build_application()
    async with application:
        update = Update.de_json(update_data, application.bot)
        await application.process_update(update)


@app.route(f"/webhook/{WEBHOOK_SECRET}", methods=["POST"])
def telegram_webhook():
    update_data = request.get_json(force=True, silent=True)
    if update_data is None:
        abort(400)
    asyncio.run(_process_update(update_data))
    return "ok"


@app.route("/")
def health_check():
    return "ASAP TeleBot webhook is running."
