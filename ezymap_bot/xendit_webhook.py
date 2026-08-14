"""Core logic for handling a Xendit invoice-paid webhook callback. Kept separate from
webhook_app.py so both the per-bot webhook_app.py and the combined_webhook_app.py can
share it without duplicating the notify-Jack-and-client logic.
"""

import logging

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

from . import content
from .config import ADMIN_CHAT_ID, BOT_TOKEN
from .invoice_store import get_invoice, mark_processed

logger = logging.getLogger(__name__)


async def handle_paid_invoice(payload: dict) -> None:
    if payload.get("status") != "PAID":
        return

    external_id = payload.get("external_id")
    if not external_id:
        return

    record = get_invoice(external_id)
    if record is None:
        logger.warning("Received Xendit webhook for unknown external_id=%s", external_id)
        return
    if record.get("processed"):
        return

    bot = Bot(token=BOT_TOKEN)

    username_line = f"@{record['username']}" if record.get("username") else "(no username set)"
    admin_text = (
        "💰 *EzyMap payment confirmed via Xendit*\n\n"
        f"Product: {record['product_name']}\n"
        f"Plan: {record['plan_name']} — {record['currency']} {record['price']}\n"
        f"Telegram username: {username_line}\n"
        f"Telegram ID: `{record['user_id']}`\n\n"
        "Payment auto-confirmed by Xendit — no action needed except activating access."
    )
    chat_with_client_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("💬 Chat with Client", url=f"tg://user?id={record['user_id']}")]]
    )
    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=admin_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=chat_with_client_keyboard,
    )

    region = record.get("region", content.DEFAULT_PRICE_REGION)
    client_text_template = content.XENDIT_AUTO_CONFIRM_CLIENT_TEXT.get(
        region, content.XENDIT_AUTO_CONFIRM_CLIENT_TEXT[content.DEFAULT_PRICE_REGION]
    )
    client_text = client_text_template.format(
        product_name=record["product_name"], plan_name=record["plan_name"]
    )
    await bot.send_message(
        chat_id=record["chat_id"], text=client_text, parse_mode=ParseMode.MARKDOWN
    )

    mark_processed(external_id)
