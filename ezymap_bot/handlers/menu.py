import os

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .. import content
from .. import keyboards
from ..keyboards import (
    currency_select_menu,
    faq_answer_keyboard,
    faq_menu,
    mt5_bundles_menu,
    payment_method_menu,
    product_detail_menu,
)
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


def _currency(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("price_currency", content.DEFAULT_CURRENCY)


async def _show_route(query, region: str, route_key: str) -> None:
    text_dict, keyboard_fn = _SIMPLE_ROUTES[route_key]
    text = _text(text_dict, region)
    reply_markup = keyboard_fn(region)
    # The tier detail screen may be a photo message (package tier image) - edit_message_text
    # fails on those, so replace the message instead of editing it in that case.
    if query.message.photo:
        await query.delete_message()
        await query.message.chat.send_message(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)


async def menu_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    region = context.user_data.get("price_region", content.DEFAULT_PRICE_REGION)

    if data in ("lang_en", "lang_my"):
        region = "en" if data == "lang_en" else "my"
        context.user_data["price_region"] = region
        await query.delete_message()
        await update.effective_chat.send_message(
            _text(content.CURRENCY_SELECT_TEXT, region), reply_markup=currency_select_menu(region)
        )
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
            reply_markup=product_detail_menu(product_code, region, _currency(context)),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if data.startswith("choose_pay_"):
        payload = data.removeprefix("choose_pay_")
        product_code, duration_code = payload.rsplit("_", 1)
        product = content.PRODUCTS.get(product_code)
        if product is None or duration_code not in product["plans"]:
            await _show_route(query, region, "menu_pro")
            return
        price = product["plans"][duration_code]
        plan_name = content.plan_duration_label(duration_code, region)
        text = _text(content.CHOOSE_PAYMENT_METHOD_TEXT, region).format(
            product_name=product["name"], plan_name=plan_name, price=content.format_price(price, _currency(context))
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
        image = content.PACKAGE_TIER_IMAGES.get(tier_key)
        if image:
            # A text message can't be edited into a photo message, so replace it instead.
            await query.delete_message()
            photo = open(image, "rb") if os.path.exists(image) else image
            try:
                await update.effective_chat.send_photo(
                    photo,
                    caption=detail_text,
                    reply_markup=keyboards.tier_detail_menu(region),
                    parse_mode=ParseMode.MARKDOWN,
                )
            finally:
                if hasattr(photo, "close"):
                    photo.close()
        else:
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
