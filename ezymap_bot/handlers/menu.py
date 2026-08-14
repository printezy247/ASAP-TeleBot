from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .. import content
from ..keyboards import (
    BACK_TO_MAIN,
    BACK_TO_PACKAGES,
    MAIN_MENU,
    PACKAGE_TIER_MENU,
    PURCHASE_CATEGORY_MENU,
    TIER_DETAIL_MENU,
    faq_answer_keyboard,
    faq_menu,
    mt5_bundles_menu,
    product_detail_menu,
)

_SIMPLE_ROUTES = {
    "menu_main": (content.MAIN_MENU_TEXT, MAIN_MENU),
    "menu_broker": (content.BROKER_INFO_TEXT, BACK_TO_MAIN),
    "menu_packages": (content.PACKAGES_INTRO_TEXT, PACKAGE_TIER_MENU),
    "menu_pro": (content.PURCHASE_INTRO_TEXT, PURCHASE_CATEGORY_MENU),
    "menu_faq": ("❓ *FAQ* — tap a question to see the answer.", None),
    "products_mt5": (content.MT5_BUNDLES_INTRO_TEXT, None),
    "reg_open_account": (content.OPEN_ACCOUNT_TEXT, BACK_TO_PACKAGES),
    "reg_change_ib": (content.CHANGE_IB_TEXT, BACK_TO_PACKAGES),
}


async def menu_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_faq":
        text, _ = _SIMPLE_ROUTES[data]
        await query.edit_message_text(text, reply_markup=faq_menu(), parse_mode=ParseMode.MARKDOWN)
        return

    if data == "products_mt5":
        text, _ = _SIMPLE_ROUTES[data]
        await query.edit_message_text(
            text, reply_markup=mt5_bundles_menu(), parse_mode=ParseMode.MARKDOWN
        )
        return

    if data.startswith("product_"):
        product_code = data.removeprefix("product_")
        if product_code not in content.PRODUCTS:
            text, keyboard = _SIMPLE_ROUTES["menu_pro"]
            await query.edit_message_text(text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
            return
        text = content.product_detail_text(product_code)
        await query.edit_message_text(
            text, reply_markup=product_detail_menu(product_code), parse_mode=ParseMode.MARKDOWN
        )
        return

    if data.startswith("tier_"):
        tier_key = data.removeprefix("tier_")
        if tier_key not in content.PACKAGE_TIERS:
            text, keyboard = _SIMPLE_ROUTES["menu_packages"]
            await query.edit_message_text(text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
            return
        context.user_data["selected_package"] = tier_key
        _tier_name, detail_text = content.PACKAGE_TIERS[tier_key]
        await query.edit_message_text(
            detail_text, reply_markup=TIER_DETAIL_MENU, parse_mode=ParseMode.MARKDOWN
        )
        return

    if data.startswith("faq_"):
        index = int(data.removeprefix("faq_"))
        question, answer, show_contact_admin = content.FAQ_ITEMS[index]
        text = f"❓ *{question}*\n\n{answer}"
        await query.edit_message_text(
            text, reply_markup=faq_answer_keyboard(show_contact_admin), parse_mode=ParseMode.MARKDOWN
        )
        return

    if data not in _SIMPLE_ROUTES:
        text, keyboard = _SIMPLE_ROUTES["menu_main"]
        await query.edit_message_text(text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
        return

    text, keyboard = _SIMPLE_ROUTES[data]
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
