"""Native Telegram Payments (via @BotFather -> Payments) for providers connected there,
e.g. iPay88 and Smart Glocal. Unlike Xendit, this needs no webhook: Telegram delivers the
pre_checkout_query and the successful_payment confirmation straight to the bot as normal
updates in the same chat the invoice was sent to.
"""

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, Update
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import ContextTypes

from .. import content
from ..config import ADMIN_CHAT_ID, IPAY88_PROVIDER_TOKEN, SMARTGLOCAL_PROVIDER_TOKEN
from ..keyboards import different_payment_method_keyboard

logger = logging.getLogger(__name__)

# provider code (matches the "natpay_<provider>_..." callback_data prefix) -> its
# BotFather-issued provider token. Add an entry here (plus the token in config.py and a
# display name in content.NATIVE_PAYMENT_PROVIDERS) to offer another provider.
_PROVIDER_TOKENS = {
    "ipay88": IPAY88_PROVIDER_TOKEN,
    "smartglocal": SMARTGLOCAL_PROVIDER_TOKEN,
}

_PAYLOAD_PREFIX = "natpay"
_INVALID_INVOICE_MESSAGE = "This invoice is no longer valid. Please start again from the bot's menu."


def _region(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("price_region", content.DEFAULT_PRICE_REGION)


def _text(text_dict: dict, region: str) -> str:
    return text_dict.get(region, text_dict[content.DEFAULT_PRICE_REGION])


def _parse_payload(payload: str):
    """Returns (provider_key, product, product_code, duration_code, region) or None if the
    payload is malformed or refers to a product/duration that no longer exists."""
    parts = (payload or "").split("|")
    if len(parts) != 5 or parts[0] != _PAYLOAD_PREFIX:
        return None
    _, provider_key, product_code, duration_code, region = parts
    product = content.PRODUCTS.get(product_code)
    if product is None or duration_code not in product["plans"]:
        return None
    return provider_key, product, product_code, duration_code, region


async def initiate_native_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    region = _region(context)

    payload = query.data.removeprefix("natpay_")
    provider_key, rest = payload.split("_", 1)
    product_code, duration_code = rest.rsplit("_", 1)
    provider_name = content.NATIVE_PAYMENT_PROVIDERS.get(provider_key, provider_key)

    product = content.PRODUCTS.get(product_code)
    if product is None or duration_code not in product["plans"]:
        await query.edit_message_text(
            _text(content.MAIN_MENU_TEXT, region), reply_markup=different_payment_method_keyboard(region)
        )
        return

    provider_token = _PROVIDER_TOKENS.get(provider_key)
    if not provider_token:
        await query.edit_message_text(
            _text(content.NATIVE_PAYMENT_UNAVAILABLE_TEXT, region).format(provider=provider_name),
            reply_markup=different_payment_method_keyboard(region),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    price = product["plans"][duration_code]
    plan_name = content.plan_duration_label(duration_code, region)
    _symbol, currency_code = content.PRICE_REGIONS.get(
        region, content.PRICE_REGIONS[content.DEFAULT_PRICE_REGION]
    )
    # USD and MYR (the only currencies this bot uses) both have 2 decimal places, so the
    # smallest unit is price * 100. Revisit this if a 0- or 3-decimal currency is ever added.
    amount_minor_units = int(round(float(price) * 100))
    invoice_payload = f"{_PAYLOAD_PREFIX}|{provider_key}|{product_code}|{duration_code}|{region}"

    try:
        await context.bot.send_invoice(
            chat_id=update.effective_chat.id,
            title=f"{product['name']} — {plan_name}",
            description=_text(product["description"], region),
            payload=invoice_payload,
            provider_token=provider_token,
            currency=currency_code,
            prices=[LabeledPrice(label=f"{product['name']} — {plan_name}", amount=amount_minor_units)],
        )
    except TelegramError:
        logger.exception(
            "Failed to send %s invoice for product=%s duration=%s to chat=%s",
            provider_name,
            product_code,
            duration_code,
            update.effective_chat.id,
        )
        await query.edit_message_text(
            _text(content.NATIVE_PAYMENT_INVOICE_FAILED_TEXT, region).format(provider=provider_name),
            reply_markup=different_payment_method_keyboard(region),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    text = _text(content.NATIVE_PAYMENT_INVOICE_SENT_TEXT, region).format(
        product_name=product["name"], plan_name=plan_name, provider=provider_name
    )
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN)


async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.pre_checkout_query
    if _parse_payload(query.invoice_payload) is None:
        await query.answer(ok=False, error_message=_INVALID_INVOICE_MESSAGE)
        return
    await query.answer(ok=True)


async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    payment = update.message.successful_payment
    parsed = _parse_payload(payment.invoice_payload)
    if parsed is None:
        logger.warning(
            "Received successful_payment with unrecognized payload=%r", payment.invoice_payload
        )
        return
    provider_key, product, _product_code, duration_code, region = parsed
    provider_name = content.NATIVE_PAYMENT_PROVIDERS.get(provider_key, provider_key)
    plan_name = content.plan_duration_label(duration_code, region)

    user = update.effective_user
    username_line = f"@{user.username}" if user.username else "(no username set)"
    # Admin-facing notification always stays in English - it's for Jack, not the client.
    admin_text = (
        f"💰 *EzyMap payment confirmed via {provider_name}*\n\n"
        f"Product: {product['name']}\n"
        f"Plan: {plan_name} — {payment.currency} {payment.total_amount / 100:.2f}\n"
        f"Telegram username: {username_line}\n"
        f"Telegram ID: `{user.id}`\n"
        f"Provider charge ID: `{payment.provider_payment_charge_id}`\n\n"
        f"Payment auto-confirmed by {provider_name} — no action needed except activating access."
    )
    chat_with_client_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("💬 Chat with Client", url=f"tg://user?id={user.id}")]]
    )

    admin_notified = True
    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=chat_with_client_keyboard,
        )
    except TelegramError:
        admin_notified = False
        logger.exception(
            "Failed to DM admin (chat_id=%s) with %s payment confirmation from user %s. "
            "The admin account must send /start to this bot at least once before it can "
            "receive DMs.",
            ADMIN_CHAT_ID,
            provider_name,
            user.id,
        )

    client_text_dict = (
        content.NATIVE_PAYMENT_AUTO_CONFIRM_CLIENT_TEXT
        if admin_notified
        else content.NATIVE_PAYMENT_AUTO_CONFIRM_ADMIN_UNREACHABLE_TEXT
    )
    client_text = _text(client_text_dict, region).format(
        product_name=product["name"], plan_name=plan_name
    )
    await update.message.reply_text(client_text, parse_mode=ParseMode.MARKDOWN)
