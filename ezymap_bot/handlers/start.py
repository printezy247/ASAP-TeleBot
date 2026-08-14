from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .. import content
from ..keyboards import LANGUAGE_SELECT_MENU, main_menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_message(
        content.LANGUAGE_SELECT_TEXT, reply_markup=LANGUAGE_SELECT_MENU
    )


async def send_greeting_and_menu(chat, region: str) -> None:
    for message in content.WELCOME_MESSAGES.get(region, content.WELCOME_MESSAGES["en"]):
        await chat.send_message(message, parse_mode=ParseMode.MARKDOWN)

    main_menu_text = content.MAIN_MENU_TEXT.get(region, content.MAIN_MENU_TEXT["en"])
    await chat.send_message(main_menu_text, reply_markup=main_menu(region))
