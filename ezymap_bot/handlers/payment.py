import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import ContextTypes, ConversationHandler

from .. import content
from ..config import ADMIN_CHAT_ID
from ..keyboards import MAIN_MENU, payment_prompt_keyboard
from .start import start

logger = logging.getLogger(__name__)

ASK_PROOF = 100


async def plan_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    payload = query.data.removeprefix("buy_")
    product_code, duration_code = payload.rsplit("_", 1)
    product = content.PRODUCTS[product_code]
    price = product["plans"][duration_code]
    plan_name = content.PLAN_DURATION_LABELS[duration_code]

    context.user_data["pay_product_name"] = product["name"]
    context.user_data["pay_plan_name"] = plan_name
    context.user_data["pay_price"] = price

    text = content.PAYMENT_PROMPT_TEMPLATE.format(
        product_name=product["name"], plan_name=plan_name, price=price, network=content.USDT_NETWORK
    )
    await query.edit_message_text(
        text, reply_markup=payment_prompt_keyboard(), parse_mode=ParseMode.MARKDOWN
    )
    return ASK_PROOF


async def receive_proof(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    product_name = context.user_data.get("pay_product_name", "-")
    plan_name = context.user_data.get("pay_plan_name", "-")
    price = context.user_data.get("pay_price", "-")
    user = update.effective_user

    username_line = f"@{user.username}" if user.username else "(no username set)"
    admin_summary = (
        "💰 *New EzyMap payment proof*\n\n"
        f"Product: {product_name}\n"
        f"Plan: {plan_name} — ${price}\n"
        f"Telegram username: {username_line}\n"
        f"Telegram ID: `{user.id}`\n\n"
        "The client's proof (screenshot/message) is forwarded below."
    )
    chat_with_client_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("💬 Chat with Client", url=f"tg://user?id={user.id}")]]
    )

    admin_notified = True
    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_summary,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=chat_with_client_keyboard,
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

    confirmation_text = (
        content.PAYMENT_PROOF_RECEIVED_TEXT
        if admin_notified
        else content.PAYMENT_PROOF_ADMIN_UNREACHABLE_TEXT
    )
    await update.message.reply_text(
        confirmation_text, reply_markup=MAIN_MENU, parse_mode=ParseMode.MARKDOWN
    )

    context.user_data.pop("pay_product_name", None)
    context.user_data.pop("pay_plan_name", None)
    context.user_data.pop("pay_price", None)
    return ConversationHandler.END


async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data.pop("pay_product_name", None)
    context.user_data.pop("pay_plan_name", None)
    context.user_data.pop("pay_price", None)
    await query.edit_message_text(
        content.MAIN_MENU_TEXT, reply_markup=MAIN_MENU, parse_mode=ParseMode.MARKDOWN
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(content.CANCEL_TEXT)
    return ConversationHandler.END


async def restart_via_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.pop("pay_product_name", None)
    context.user_data.pop("pay_plan_name", None)
    context.user_data.pop("pay_price", None)
    await start(update, context)
    return ConversationHandler.END
