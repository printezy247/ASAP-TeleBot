from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .. import content
from ..keyboards import (
    BACK_TO_DEPOSIT,
    BACK_TO_FAQ,
    BACK_TO_MAIN,
    BACK_TO_SIGNALS,
    DEPOSIT_MENU,
    MAIN_MENU,
    SIGNALS_MENU,
    faq_menu,
)

_SIMPLE_ROUTES = {
    "menu_main": (content.MAIN_MENU_TEXT, MAIN_MENU),
    "menu_broker": (content.BROKER_INFO_TEXT, BACK_TO_MAIN),
    "menu_signals": (content.SIGNALS_INTRO_TEXT, SIGNALS_MENU),
    "menu_faq": ("❓ *FAQ* — tap a question to see the answer.", None),
    "reg_open_account": (content.OPEN_ACCOUNT_TEXT, BACK_TO_SIGNALS),
    "reg_change_ib": (content.CHANGE_IB_TEXT, BACK_TO_SIGNALS),
    "reg_deposit": (content.DEPOSIT_INTRO_TEXT, DEPOSIT_MENU),
    "reg_withdraw": (content.WITHDRAW_TEXT, BACK_TO_SIGNALS),
    "deposit_bank": (content.DEPOSIT_BANK_TEXT, BACK_TO_DEPOSIT),
    "deposit_card": (content.DEPOSIT_CARD_TEXT, BACK_TO_DEPOSIT),
    "deposit_btc": (content.DEPOSIT_BTC_TEXT, BACK_TO_DEPOSIT),
    "deposit_usdt": (content.DEPOSIT_USDT_TEXT, BACK_TO_DEPOSIT),
}


async def menu_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_faq":
        text, _ = _SIMPLE_ROUTES[data]
        await query.edit_message_text(text, reply_markup=faq_menu(), parse_mode=ParseMode.MARKDOWN)
        return

    if data.startswith("faq_"):
        index = int(data.removeprefix("faq_"))
        question, answer = content.FAQ_ITEMS[index]
        text = f"❓ *{question}*\n\n{answer}"
        await query.edit_message_text(text, reply_markup=BACK_TO_FAQ, parse_mode=ParseMode.MARKDOWN)
        return

    text, keyboard = _SIMPLE_ROUTES[data]
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
