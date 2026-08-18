from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from .. import content
from ..fx_rates import is_known_currency
from .start import send_greeting_and_menu, start

ASK_CURRENCY_CODE = 200


def _region(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("price_region", content.DEFAULT_PRICE_REGION)


def _text(text_dict: dict, region: str) -> str:
    return text_dict.get(region, text_dict[content.DEFAULT_PRICE_REGION])


async def currency_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles a tap on one of the curated quick-pick currency buttons."""
    query = update.callback_query
    await query.answer()
    context.user_data["price_currency"] = query.data.removeprefix("currency_")
    await query.delete_message()
    await send_greeting_and_menu(update.effective_chat, _region(context))


async def prompt_currency_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point for "🌐 Other Currency" - asks the client to type any ISO code."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(_text(content.ASK_CURRENCY_CODE_TEXT, _region(context)))
    return ASK_CURRENCY_CODE


async def receive_currency_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    region = _region(context)
    code = update.message.text.strip().lower()
    if len(code) != 3 or not code.isalpha() or not is_known_currency(code):
        await update.message.reply_text(_text(content.CURRENCY_NOT_RECOGNIZED_TEXT, region))
        return ASK_CURRENCY_CODE

    context.user_data["price_currency"] = code
    await send_greeting_and_menu(update.effective_chat, region)
    return ConversationHandler.END


async def cancel_currency_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Graceful default rather than leaving the client stuck mid-setup with no
    # currency chosen at all.
    context.user_data["price_currency"] = content.DEFAULT_CURRENCY
    await send_greeting_and_menu(update.effective_chat, _region(context))
    return ConversationHandler.END


async def restart_via_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await start(update, context)
    return ConversationHandler.END
