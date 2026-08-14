import logging
import uuid

import httpx
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .. import content
from ..config import XENDIT_SECRET_KEY
from ..invoice_store import save_invoice
from ..keyboards import different_payment_method_keyboard, xendit_invoice_keyboard
from ..xendit_client import create_invoice

logger = logging.getLogger(__name__)


def _region(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("price_region", content.DEFAULT_PRICE_REGION)


def _text(text_dict: dict, region: str) -> str:
    return text_dict.get(region, text_dict[content.DEFAULT_PRICE_REGION])


async def initiate_xendit_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    region = _region(context)

    payload = query.data.removeprefix("xendit_")
    product_code, duration_code = payload.rsplit("_", 1)

    product = content.PRODUCTS.get(product_code)
    if product is None or duration_code not in product["plans"]:
        await query.edit_message_text(
            _text(content.MAIN_MENU_TEXT, region), reply_markup=different_payment_method_keyboard(region)
        )
        return

    if not XENDIT_SECRET_KEY:
        await query.edit_message_text(
            _text(content.XENDIT_UNAVAILABLE_TEXT, region),
            reply_markup=different_payment_method_keyboard(region),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    price = product["plans"][duration_code]
    plan_name = content.plan_duration_label(duration_code, region)
    symbol, currency_code = content.PRICE_REGIONS.get(
        region, content.PRICE_REGIONS[content.DEFAULT_PRICE_REGION]
    )

    user = update.effective_user
    external_id = f"ezymap-{user.id}-{product_code}-{duration_code}-{uuid.uuid4().hex[:8]}"

    try:
        invoice = await create_invoice(
            external_id=external_id,
            amount=float(price),
            currency=currency_code,
            description=f"{product['name']} — {plan_name}",
        )
    except httpx.HTTPError:
        logger.exception("Failed to create Xendit invoice for %s", external_id)
        await query.edit_message_text(
            _text(content.XENDIT_INVOICE_FAILED_TEXT, region),
            reply_markup=different_payment_method_keyboard(region),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    save_invoice(
        external_id,
        {
            "chat_id": update.effective_chat.id,
            "user_id": user.id,
            "username": user.username,
            "product_code": product_code,
            "product_name": product["name"],
            "duration_code": duration_code,
            "plan_name": plan_name,
            "price": price,
            "currency": currency_code,
            "region": region,
            "processed": False,
        },
    )

    text = _text(content.XENDIT_INVOICE_CREATED_TEXT, region).format(
        product_name=product["name"], plan_name=plan_name, price=f"{symbol}{price}"
    )
    await query.edit_message_text(
        text,
        reply_markup=xendit_invoice_keyboard(invoice["invoice_url"], region),
        parse_mode=ParseMode.MARKDOWN,
    )
