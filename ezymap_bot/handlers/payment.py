import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import ContextTypes, ConversationHandler

from .. import content
from ..config import ADMIN_CHAT_ID
from ..keyboards import main_menu, payment_prompt_keyboard
from ..receipt import payment_receipt
from ..receipt_utils import generate_receipt_number
from .start import start

logger = logging.getLogger(__name__)

ASK_PROOF = 100


def _region(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("price_region", content.DEFAULT_PRICE_REGION)


def _text(text_dict: dict, region: str) -> str:
    return text_dict.get(region, text_dict[content.DEFAULT_PRICE_REGION])


async def plan_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    region = _region(context)

    payload = query.data.removeprefix("buy_")
    product_code, duration_code = payload.rsplit("_", 1)
    product = content.PRODUCTS[product_code]
    price = product["plans"][duration_code]
    plan_name = content.plan_duration_label(duration_code, region)

    context.user_data["pay_product_code"] = product_code
    context.user_data["pay_duration_code"] = duration_code
    context.user_data["pay_product_name"] = product["name"]
    context.user_data["pay_plan_name"] = plan_name
    context.user_data["pay_price"] = price

    text = _text(content.PAYMENT_PROMPT_TEMPLATE, region).format(
        product_name=product["name"], plan_name=plan_name, price=price, network=content.USDT_NETWORK
    )
    await query.edit_message_text(
        text, reply_markup=payment_prompt_keyboard(region), parse_mode=ParseMode.MARKDOWN
    )
    return ASK_PROOF


async def receive_proof(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    region = _region(context)
    product_code = context.user_data.get("pay_product_code", "-")
    duration_code = context.user_data.get("pay_duration_code", "-")
    product_name = context.user_data.get("pay_product_name", "-")
    plan_name = context.user_data.get("pay_plan_name", "-")
    price = context.user_data.get("pay_price", "-")
    user = update.effective_user

    # Admin-facing notification always stays in English - it's for Jack, not the client.
    username_line = f"@{user.username}" if user.username else "(no username set)"
    admin_summary = (
        "💰 *New EzyMap payment proof*\n\n"
        f"Product: {product_name}\n"
        f"Plan: {plan_name} — ${price}\n"
        f"Telegram username: {username_line}\n"
        f"Telegram ID: `{user.id}`\n\n"
        "The client's proof (screenshot/message) is forwarded below.\n\n"
        "Once you've verified the transfer, tap Confirm Payment below to send the "
        "client their receipt."
    )
    admin_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💬 Chat with Client", url=f"tg://user?id={user.id}")],
            [
                InlineKeyboardButton(
                    "✅ Confirm Payment",
                    callback_data=f"confirmusdt|{update.effective_chat.id}|{product_code}|{duration_code}|{region}",
                )
            ],
        ]
    )

    admin_notified = True
    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_summary,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=admin_keyboard,
        )
        await context.bot.forward_message(
            chat_id=ADMIN_CHAT_ID,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id,
        )
    except TelegramError:
        admin_notified = False
        logger.exception(
            "Failed to DM admin (chat_id=%s) with payment proof from user %s. The admin "
            "account must send /start to this bot at least once before it can receive DMs.",
            ADMIN_CHAT_ID,
            user.id,
        )

    confirmation_text = _text(
        content.PAYMENT_PROOF_RECEIVED_TEXT if admin_notified else content.PAYMENT_PROOF_ADMIN_UNREACHABLE_TEXT,
        region,
    )
    await update.message.reply_text(
        confirmation_text, reply_markup=main_menu(region), parse_mode=ParseMode.MARKDOWN
    )

    context.user_data.pop("pay_product_code", None)
    context.user_data.pop("pay_duration_code", None)
    context.user_data.pop("pay_product_name", None)
    context.user_data.pop("pay_plan_name", None)
    context.user_data.pop("pay_price", None)
    return ConversationHandler.END


async def confirm_usdt_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    try:
        _prefix, client_chat_id, product_code, duration_code, region = query.data.split("|")
        client_chat_id = int(client_chat_id)
    except ValueError:
        logger.error("Unrecognized confirmusdt callback_data: %r", query.data)
        return

    product = content.PRODUCTS.get(product_code)
    if product is None:
        await query.edit_message_text(f"{query.message.text}\n\n⚠️ Unknown product, couldn't send receipt.")
        return

    price = product["plans"][duration_code]
    plan_name = content.plan_duration_label(duration_code, region)
    payment_method_label = "USDT"

    receipt_png = payment_receipt(
        product_name=product["name"],
        plan_name=plan_name,
        price=price,
        currency_symbol="$",
        payment_method=payment_method_label,
        receipt_number=generate_receipt_number(),
        region=region,
    )

    caption = _text(content.TG_PAYMENT_AUTO_CONFIRM_CLIENT_TEXT, region).format(
        product_name=product["name"], plan_name=plan_name
    )

    try:
        await context.bot.send_photo(
            chat_id=client_chat_id, photo=receipt_png, caption=caption, parse_mode=ParseMode.MARKDOWN
        )
    except TelegramError:
        logger.exception("Failed to send USDT payment receipt to client chat_id=%s", client_chat_id)

    try:
        await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=receipt_png, caption="Copy of client's receipt")
    except TelegramError:
        logger.exception("Failed to send USDT payment receipt copy to admin")

    await query.edit_message_reply_markup(reply_markup=None)
    await query.message.reply_text("✅ Confirmed — receipt sent to the client.")


async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    region = _region(context)
    context.user_data.pop("pay_product_name", None)
    context.user_data.pop("pay_plan_name", None)
    context.user_data.pop("pay_price", None)
    await query.edit_message_text(
        _text(content.MAIN_MENU_TEXT, region), reply_markup=main_menu(region), parse_mode=ParseMode.MARKDOWN
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(_text(content.CANCEL_TEXT, _region(context)))
    return ConversationHandler.END


async def restart_via_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.pop("pay_product_name", None)
    context.user_data.pop("pay_plan_name", None)
    context.user_data.pop("pay_price", None)
    await start(update, context)
    return ConversationHandler.END
