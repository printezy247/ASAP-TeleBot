from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .. import content
from ..keyboards import LANGUAGE_SELECT_MENU


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for message in content.WELCOME_MESSAGES:
        await update.effective_chat.send_message(message, parse_mode=ParseMode.MARKDOWN)

    await update.effective_chat.send_message(
        content.LANGUAGE_SELECT_TEXT, reply_markup=LANGUAGE_SELECT_MENU
    )
