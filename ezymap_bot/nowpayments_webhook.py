"""Core logic for handling a NOWPayments IPN (Instant Payment Notification) webhook
callback. Kept separate from webhook_app.py so both the per-bot webhook_app.py and the
combined_webhook_app.py can share it without duplicating the notify-Jack-and-client
logic.
"""

import hashlib
import hmac
import json
import logging

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.error import TelegramError

from . import content
from .config import ADMIN_CHAT_ID, BOT_TOKEN, NOWPAYMENTS_IPN_SECRET
from .invoice_store import get_invoice, mark_processed
from .receipt import generate_receipt_image

logger = logging.getLogger(__name__)

# NOWPayments' final "money has settled" state. Other statuses (waiting, confirming,
# confirmed, sending, partially_paid) are intermediate steps on the way there - acting
# on "finished" only avoids notifying the client before funds have actually arrived.
_FINISHED_STATUS = "finished"


def verify_signature(raw_body: bytes, signature: str) -> bool:
    """NOWPayments signs the IPN body as HMAC-SHA512 of the JSON payload with its keys
    recursively sorted (not the raw body as received) - see their IPN docs. Returns
    False (rather than raising) on any malformed input, so callers can just 401 it.
    """
    if not NOWPAYMENTS_IPN_SECRET or not signature:
        return False
    try:
        payload = json.loads(raw_body)
    except ValueError:
        return False
    sorted_body = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    expected = hmac.new(
        NOWPAYMENTS_IPN_SECRET.encode(), sorted_body.encode(), hashlib.sha512
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


async def handle_paid_invoice(payload: dict) -> None:
    if payload.get("payment_status") != _FINISHED_STATUS:
        return

    order_id = payload.get("order_id")
    if not order_id:
        return

    record = get_invoice(order_id)
    if record is None:
        logger.warning("Received NOWPayments webhook for unknown order_id=%s", order_id)
        return
    if record.get("processed"):
        return

    username_line = f"@{record['username']}" if record.get("username") else "(no username set)"
    admin_text = (
        "💰 *EzyMap payment confirmed via card*\n\n"
        f"Product: {record['product_name']}\n"
        f"Plan: {record['plan_name']} (${record['price']})\n"
        f"Telegram username: {username_line}\n"
        f"Telegram ID: `{record['user_id']}`\n\n"
        "Payment auto-confirmed by NOWPayments. No action needed except activating access."
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
                "Failed to DM admin (chat_id=%s) with NOWPayments confirmation for "
                "order_id=%s. The admin account must send /start to this bot at "
                "least once before it can receive DMs.",
                ADMIN_CHAT_ID,
                order_id,
            )

        region = record.get("region", content.DEFAULT_PRICE_REGION)
        label = f"{record['product_name']} ({record['plan_name']})"
        client_text_dict = (
            content.PAYMENT_APPROVED_TEXT if admin_notified else content.PAYMENT_PROOF_ADMIN_UNREACHABLE_TEXT
        )
        client_text = client_text_dict.get(region, client_text_dict[content.DEFAULT_PRICE_REGION])
        if admin_notified:
            client_text = client_text.format(label=label)

        try:
            try:
                receipt = generate_receipt_image(
                    kind="payment", region=region, name=record.get("name") or "-", label=label
                )
                await bot.send_photo(
                    chat_id=record["chat_id"], photo=receipt, caption=client_text, parse_mode=ParseMode.MARKDOWN
                )
            except TelegramError:
                raise
            except Exception:
                # Same fallback as handlers/decision.py - receipt rendering failing
                # shouldn't leave the client with no confirmation at all.
                logger.exception(
                    "Failed to generate/send receipt image for order_id=%s, falling back to text", order_id
                )
                await bot.send_message(
                    chat_id=record["chat_id"], text=client_text, parse_mode=ParseMode.MARKDOWN
                )
        except TelegramError:
            logger.exception(
                "Failed to notify client (chat_id=%s) of NOWPayments confirmation for order_id=%s",
                record["chat_id"],
                order_id,
            )

    mark_processed(order_id)
