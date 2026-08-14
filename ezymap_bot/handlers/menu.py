from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .. import content
from .. import keyboards
from ..keyboards import faq_answer_keyboard, faq_menu, mt5_bundles_menu, payment_method_menu, product_detail_menu
from .start import send_greeting_and_menu

_SIMPLE_ROUTES = {
    "menu_main": (content.MAIN_MENU_TEXT, keyboards.main_menu),
    "menu_broker": (content.BROKER_INFO_TEXT, keyboards.back_to_main),
    "menu_packages": (content.PACKAGES_INTRO_TEXT, keyboards.package_tier_menu),
    "menu_pro": (content.PURCHASE_INTRO_TEXT, keyboards.purchase_category_menu),
    "reg_open_account": (content.OPEN_ACCOUNT_TEXT, keyboards.back_to_packages),
    "reg_change_ib": (content.CHANGE_IB_TEXT, keyboards.back_to_packages),
}


def _text(text_dict: dict, region: str) -> str:
    return text_dict.get(region, text_dict[content.DEFAULT_PRICE_REGION])


async def _show_route(query, region: str, route_key: str) -> None:
    text_dict, keyboard_fn = _SIMPLE_ROUTES[route_key]
    await query.edit_message_text(
        _text(text_dict, region), reply_markup=keyboard_fn(region), parse_mode=ParseMode.MARKDOWN
    )


async def menu_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    region = context.user_data.get("price_region", content.DEFAULT_PRICE_REGION)

    if data in ("lang_en", "lang_my"):
        region = "en" if data == "lang_en" else "my"
        context.user_data["price_region"] = region
        await query.delete_message()
        await send_greeting_and_menu(update.effective_chat, region)
        return

    if data == "menu_faq":
        await query.edit_message_text(
            _text(content.FAQ_LIST_HEADER, region),
            reply_markup=faq_menu(region),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if data == "products_mt5":
        await query.edit_message_text(
            _text(content.MT5_BUNDLES_INTRO_TEXT, region),
            reply_markup=mt5_bundles_menu(region),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if data.startswith("product_"):
        product_code = data.removeprefix("product_")
        if product_code not in content.PRODUCTS:
            await _show_route(query, region, "menu_pro")
            return
        text = content.product_detail_text(product_code, region)
        await query.edit_message_text(
            text,
            reply_markup=product_detail_menu(product_code, region),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if data.startswith("choose_pay_"):
        payload = data.removeprefix("choose_pay_")
        product_code, duration_code = payload.rsplit("_", 1)
        if product_code not in content.PRODUCTS:
            await _show_route(query, region, "menu_pro")
            return
        product = content.PRODUCTS[product_code]
        price = product["plans"][duration_code]
        symbol, _currency_code = content.PRICE_REGIONS.get(
            region, content.PRICE_REGIONS[content.DEFAULT_PRICE_REGION]
        )
        plan_name = content.plan_duration_label(duration_code, region)
        text = _text(content.CHOOSE_PAYMENT_METHOD_TEXT, region).format(
            product_name=product["name"], plan_name=plan_name, price=f"{symbol}{price}"
        )
        await query.edit_message_text(
            text,
            reply_markup=payment_method_menu(product_code, duration_code, region),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if data.startswith("tier_"):
        tier_key = data.removeprefix("tier_")
        if tier_key not in content.PACKAGE_TIERS:
            await _show_route(query, region, "menu_packages")
            return
        context.user_data["selected_package"] = tier_key
        detail_text = _text(content.PACKAGE_TIERS[tier_key]["detail"], region)
        await query.edit_message_text(
            detail_text, reply_markup=keyboards.tier_detail_menu(region), parse_mode=ParseMode.MARKDOWN
        )
        return

    if data.startswith("faq_"):
        index = int(data.removeprefix("faq_"))
        item = content.FAQ_ITEMS[index]
        question = _text(item["question"], region)
        answer = _text(item["answer"], region)
        text = f"❓ *{question}*\n\n{answer}"
        await query.edit_message_text(
            text,
            reply_markup=faq_answer_keyboard(item["show_contact_admin"], item["extra_button"], region),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if data not in _SIMPLE_ROUTES:
        await _show_route(query, region, "menu_main")
        return

    await _show_route(query, region, data)
