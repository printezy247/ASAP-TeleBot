"""Single Flask app that serves BOTH bots' webhooks, so a free PythonAnywhere
account (limited to one web app) can host both without paying for a second one.

Each bot keeps its own route, its own secret, and its own Application/persistence
file - this file just multiplexes incoming requests to the right one.
"""

import asyncio
import logging

from flask import Flask, abort, request
from telegram import Update

from asap_telebot.config import WEBHOOK_SECRET as ASAP_WEBHOOK_SECRET
from asap_telebot.main import build_application as build_asap_application
from ezymap_bot.config import WEBHOOK_SECRET as EZYMAP_WEBHOOK_SECRET
from ezymap_bot.main import build_application as build_ezymap_application
from ezymap_bot.nowpayments_webhook import handle_paid_invoice as handle_nowpayments_invoice
from ezymap_bot.nowpayments_webhook import verify_signature as verify_nowpayments_signature

if not ASAP_WEBHOOK_SECRET:
    raise RuntimeError("WEBHOOK_SECRET is not set. Add it to .env (see .env.example).")
if not EZYMAP_WEBHOOK_SECRET:
    raise RuntimeError("EZYMAP_WEBHOOK_SECRET is not set. Add it to .env (see .env.example).")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

app = Flask(__name__)


async def _process_update(build_application, update_data: dict) -> None:
    application = build_application()
    async with application:
        update = Update.de_json(update_data, application.bot)
        await application.process_update(update)


def _handle_webhook(build_application):
    update_data = request.get_json(force=True, silent=True)
    if update_data is None:
        abort(400)
    asyncio.run(_process_update(build_application, update_data))
    return "ok"


@app.route(f"/webhook/asap/{ASAP_WEBHOOK_SECRET}", methods=["POST"])
def asap_webhook():
    return _handle_webhook(build_asap_application)


@app.route(f"/webhook/ezymap/{EZYMAP_WEBHOOK_SECRET}", methods=["POST"])
def ezymap_webhook():
    return _handle_webhook(build_ezymap_application)


@app.route("/nowpayments/webhook", methods=["POST"])
def nowpayments_webhook():
    raw_body = request.get_data()
    signature = request.headers.get("x-nowpayments-sig", "")
    if not verify_nowpayments_signature(raw_body, signature):
        abort(401)
    payload = request.get_json(force=True, silent=True)
    if payload is None:
        abort(400)
    asyncio.run(handle_nowpayments_invoice(payload))
    return "ok"


@app.route("/")
def health_check():
    return "ASAP-TeleBot combined webhook (asap_telebot + ezymap_bot) is running."
