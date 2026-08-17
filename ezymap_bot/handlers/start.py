from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .. import content
from ..keyboards import LANGUAGE_SELECT_MENU, main_menu, package_tier_menu, payment_method_menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args and await _handle_deep_link(update, context, context.args[0]):
        return

    await update.effective_chat.send_message(
        content.LANGUAGE_SELECT_TEXT, reply_markup=LANGUAGE_SELECT_MENU
    )


async def _handle_deep_link(update: Update, context: ContextTypes.DEFAULT_TYPE, payload: str) -> bool:
    """Handle recognized /start deep-link payloads, jumping straight past the
    language/menu flow. Used by external bots (e.g. the Sarah keyword bot)
    linking straight to a specific screen. Returns True if the payload was
    recognized and handled.

    Formats:
      buy_<lang>_<duration>_<product_code>  -> straight to that product's
                                                payment-method screen
      free_<lang>                           -> straight to the free package
                                                tier picker
    """
    parts = payload.split("_")

    if len(parts) == 2 and parts[0] == "free":
        _, lang = parts
        region = "my" if lang == "my" else "en"
        context.user_data["price_region"] = region
        text = content.PACKAGES_INTRO_TEXT.get(
            region, content.PACKAGES_INTRO_TEXT[content.DEFAULT_PRICE_REGION]
        )
        await update.effective_chat.send_message(
            text, reply_markup=package_tier_menu(region), parse_mode=ParseMode.MARKDOWN
        )
        return True

    if len(parts) >= 4 and parts[0] == "buy":
        _, lang, duration, product_code = payload.split("_", 3)
        region = "my" if lang == "my" else "en"

        product = content.PRODUCTS.get(product_code)
        if not product or duration not in product["plans"]:
            return False

        context.user_data["price_region"] = region

        symbol = content.PRICE_REGIONS.get(region, content.PRICE_REGIONS[content.DEFAULT_PRICE_REGION])
        price = product["plans"][duration]
        plan_name = content.plan_duration_label(duration, region)
        text = content.CHOOSE_PAYMENT_METHOD_TEXT.get(
            region, content.CHOOSE_PAYMENT_METHOD_TEXT[content.DEFAULT_PRICE_REGION]
        ).format(product_name=product["name"], plan_name=plan_name, price=f"{symbol}{price}")

        await update.effective_chat.send_message(
            text,
            reply_markup=payment_method_menu(product_code, duration, region),
            parse_mode=ParseMode.MARKDOWN,
        )
        return True

    return False


async def send_greeting_and_menu(chat, region: str) -> None:
    for message in content.WELCOME_MESSAGES.get(region, content.WELCOME_MESSAGES["en"]):
        await chat.send_message(message, parse_mode=ParseMode.MARKDOWN)

    main_menu_text = content.MAIN_MENU_TEXT.get(region, content.MAIN_MENU_TEXT["en"])
    await chat.send_message(main_menu_text, reply_markup=main_menu(region))
