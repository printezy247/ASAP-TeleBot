import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import ContextTypes, ConversationHandler

from .. import content
from ..config import ADMIN_CHAT_ID
from ..keyboards import MAIN_MENU
from .start import start

logger = logging.getLogger(__name__)

ASK_NAME, ASK_EMAIL, ASK_ACCOUNT = range(3)


async def submit_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(content.SUBMIT_DETAILS_PROMPT, parse_mode=ParseMode.MARKDOWN)
    return ASK_NAME


async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["reg_name"] = update.message.text.strip()
    await update.message.reply_text(content.ASK_EMAIL_TEXT, parse_mode=ParseMode.MARKDOWN)
    return ASK_EMAIL


async def receive_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["reg_email"] = update.message.text.strip()
    await update.message.reply_text(content.ASK_ACCOUNT_TEXT, parse_mode=ParseMode.MARKDOWN)
    return ASK_ACCOUNT


async def receive_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["reg_account"] = update.message.text.strip()

    name = context.user_data.get("reg_name", "-")
    email = context.user_data.get("reg_email", "-")
    account = context.user_data.get("reg_account", "-")
    user = update.effective_user

    username_line = f"@{user.username}" if user.username else "(no username set)"
    admin_text = (
        "📥 *New registration submission*\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Account Number: {account}\n\n"
        f"Telegram username: {username_line}\n"
        f"Telegram ID: `{user.id}`"
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
            "Failed to DM admin (chat_id=%s) with registration submission from user %s. "
            "The admin account must send /start to this bot at least once before it can "
            "receive DMs.",
            ADMIN_CHAT_ID,
            user.id,
        )

    confirmation_text = (
        content.SUBMISSION_CONFIRMATION_TEXT
        if admin_notified
        else content.SUBMISSION_ADMIN_UNREACHABLE_TEXT
    )
    await update.message.reply_text(
        confirmation_text,
        reply_markup=MAIN_MENU,
        parse_mode=ParseMode.MARKDOWN,
    )

    context.user_data.pop("reg_name", None)
    context.user_data.pop("reg_email", None)
    context.user_data.pop("reg_account", None)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(content.CANCEL_TEXT, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def restart_via_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.pop("reg_name", None)
    context.user_data.pop("reg_email", None)
    context.user_data.pop("reg_account", None)
    await start(update, context)
    return ConversationHandler.END
