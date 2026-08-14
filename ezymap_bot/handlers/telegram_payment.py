import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, Update
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import ContextTypes

from .. import content
from ..config import ADMIN_CHAT_ID, TELEGRAM_PAYMENT_PROVIDER_TOKEN
from ..keyboards import different_payment_method_keyboard
from ..receipt import payment_receipt
from ..receipt_utils import generate_receipt_number

logger = logging.getLogger(__name__)


def _region(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("price_region", content.DEFAULT_PRICE_REGION)


def _text(text_dict: dict, region: str) -> str:
    return text_dict.get(region, text_dict[content.DEFAULT_PRICE_REGION])


async def initiate_telegram_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    region = _region(context)

    payload = query.data.removeprefix("tgpay_")
    product_code, duration_code = payload.rsplit("_", 1)

    if product_code not in content.PRODUCTS:
        await query.edit_message_text(
            _text(content.MAIN_MENU_TEXT, region), reply_markup=different_payment_method_keyboard(region)
        )
        return

    if not TELEGRAM_PAYMENT_PROVIDER_TOKEN:
        await query.edit_message_text(
            _text(content.TG_PAYMENT_UNAVAILABLE_TEXT, region),
            reply_markup=different_payment_method_keyboard(region),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    product = content.PRODUCTS[product_code]
    price = product["plans"][duration_code]
    plan_name = content.plan_duration_label(duration_code, region)
    _symbol, currency_code = content.PRICE_REGIONS.get(
        region, content.PRICE_REGIONS[content.DEFAULT_PRICE_REGION]
    )

    title = _text(content.TG_PAYMENT_INVOICE_TITLE, region).format(
        product_name=product["name"], plan_name=plan_name
    )
    description = _text(content.TG_PAYMENT_INVOICE_DESCRIPTION, region).format(
        product_name=product["name"], plan_name=plan_name
    )
    # invoice_payload is our own opaque string, returned back to us in the
    # successful_payment update - encodes everything we need to know what was bought.
    invoice_payload = f"{product_code}|{duration_code}|{region}"
    # Telegram Payments amounts are in the smallest currency unit (e.g. sen for MYR).
    amount_minor_units = int(round(float(price) * 100))

    try:
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        await context.bot.send_invoice(
            chat_id=update.effective_chat.id,
            title=title,
            description=description,
            payload=invoice_payload,
            provider_token=TELEGRAM_PAYMENT_PROVIDER_TOKEN,
            currency=currency_code,
            prices=[LabeledPrice(label=title, amount=amount_minor_units)],
        )
    except TelegramError:
        logger.exception(
            "Failed to send Telegram Payments invoice for product=%s duration=%s currency=%s",
            product_code,
            duration_code,
            currency_code,
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=_text(content.TG_PAYMENT_UNAVAILABLE_TEXT, region),
            reply_markup=different_payment_method_keyboard(region),
            parse_mode=ParseMode.MARKDOWN,
        )


async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.pre_checkout_query
    # No extra validation needed - the payload is our own opaque product/duration/region
    # string and every product+duration combination is always valid to buy.
    await query.answer(ok=True)


async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    payment = update.message.successful_payment
    try:
        product_code, duration_code, region = payment.invoice_payload.split("|")
    except ValueError:
        logger.error("Unrecognized successful_payment payload: %r", payment.invoice_payload)
        return

    product = content.PRODUCTS.get(product_code)
    product_name = product["name"] if product else product_code
    plan_name = content.plan_duration_label(duration_code, region) if product else duration_code
    user = update.effective_user
    amount_display = f"{payment.total_amount / 100:.2f}"

    # Admin-facing notification always stays in English - it's for Jack, not the client.
    username_line = f"@{user.username}" if user.username else "(no username set)"
    admin_text = (
        "💰 *EzyMap payment confirmed via Telegram Payments*\n\n"
        f"Product: {product_name}\n"
        f"Plan: {plan_name} — {payment.currency} {amount_display}\n"
        f"Telegram username: {username_line}\n"
        f"Telegram ID: `{user.id}`\n\n"
        "Payment auto-confirmed by Telegram — no action needed except activating access. "
        "Client's receipt is attached below."
    )
    chat_with_client_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("💬 Chat with Client", url=f"tg://user?id={user.id}")]]
    )

    _symbol, _currency_code = content.PRICE_REGIONS.get(
        region, content.PRICE_REGIONS[content.DEFAULT_PRICE_REGION]
    )
    receipt_png = payment_receipt(
        product_name=product_name,
        plan_name=plan_name,
        price=amount_display,
        currency_symbol=_symbol,
        payment_method="Card/Bank/E-Wallet",
        receipt_number=generate_receipt_number(),
        region=region,
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=chat_with_client_keyboard,
        )
        await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=receipt_png)
    except TelegramError:
        logger.exception(
            "Failed to DM admin (chat_id=%s) about a confirmed Telegram Payments purchase "
            "from user %s.",
            ADMIN_CHAT_ID,
            user.id,
        )

    client_caption = _text(content.TG_PAYMENT_AUTO_CONFIRM_CLIENT_TEXT, region).format(
        product_name=product_name, plan_name=plan_name
    )
    await update.message.reply_photo(photo=receipt_png, caption=client_caption, parse_mode=ParseMode.MARKDOWN)
