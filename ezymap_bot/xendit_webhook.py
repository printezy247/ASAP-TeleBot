"""Core logic for handling a Xendit invoice-paid webhook callback. Kept separate from
webhook_app.py so both the per-bot webhook_app.py and the combined_webhook_app.py can
share it without duplicating the notify-Jack-and-client logic.
"""

import logging

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.error import TelegramError

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

    async with Bot(token=BOT_TOKEN) as bot:
        admin_notified = True
        try:
            await bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=admin_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=chat_with_client_keyboard,
            )
        except TelegramError:
            admin_notified = False
            logger.exception(
                "Failed to DM admin (chat_id=%s) with Xendit payment confirmation for "
                "external_id=%s. The admin account must send /start to this bot at "
                "least once before it can receive DMs.",
                ADMIN_CHAT_ID,
                external_id,
            )

        region = record.get("region", content.DEFAULT_PRICE_REGION)
        client_text_dict = (
            content.XENDIT_AUTO_CONFIRM_CLIENT_TEXT
            if admin_notified
            else content.XENDIT_AUTO_CONFIRM_ADMIN_UNREACHABLE_TEXT
        )
        client_text = client_text_dict.get(
            region, client_text_dict[content.DEFAULT_PRICE_REGION]
        ).format(product_name=record["product_name"], plan_name=record["plan_name"])
        await bot.send_message(
            chat_id=record["chat_id"], text=client_text, parse_mode=ParseMode.MARKDOWN
        )

    mark_processed(external_id)
