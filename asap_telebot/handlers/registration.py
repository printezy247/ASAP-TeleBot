from telegram import ReplyKeyboardRemove, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from .. import content
from ..config import ADMIN_CHAT_ID
from ..keyboards import MAIN_MENU

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

    telegram_line = f"Telegram: @{user.username} (id: {user.id})" if user.username else f"Telegram id: {user.id}"
    admin_text = (
        "📥 *New registration submission*\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Account Number: {account}\n\n"
        f"{telegram_line}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID, text=admin_text, parse_mode=ParseMode.MARKDOWN
    )

    await update.message.reply_text(
        content.SUBMISSION_CONFIRMATION_TEXT,
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
