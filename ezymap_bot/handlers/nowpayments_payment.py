import logging
import uuid

import httpx
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .. import content
from ..config import EZYMAP_PUBLIC_BASE_URL, NOWPAYMENTS_API_KEY
from ..invoice_store import save_invoice
from ..keyboards import card_invoice_keyboard, main_menu
from ..nowpayments_client import create_invoice

logger = logging.getLogger(__name__)


def _region(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("price_region", content.DEFAULT_PRICE_REGION)


def _text(text_dict: dict, region: str) -> str:
    return text_dict.get(region, text_dict[content.DEFAULT_PRICE_REGION])


async def initiate_card_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    region = _region(context)

    payload = query.data.removeprefix("card_")
    product_code, duration_code = payload.rsplit("_", 1)

    product = content.PRODUCTS.get(product_code)
    if product is None or duration_code not in product["plans"]:
        await query.edit_message_text(
            _text(content.MAIN_MENU_TEXT, region), reply_markup=main_menu(region), parse_mode=ParseMode.MARKDOWN
        )
        return

    if not NOWPAYMENTS_API_KEY or not EZYMAP_PUBLIC_BASE_URL:
        await query.edit_message_text(
            _text(content.CARD_UNAVAILABLE_TEXT, region),
            reply_markup=main_menu(region),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    price = product["plans"][duration_code]
    plan_name = content.plan_duration_label(duration_code, region)

    user = update.effective_user
    order_id = f"ezymap-{user.id}-{product_code}-{duration_code}-{uuid.uuid4().hex[:8]}"

    try:
        invoice = await create_invoice(
            order_id=order_id,
            amount=float(price),
            description=f"{product['name']} ({plan_name})",
            ipn_callback_url=f"{EZYMAP_PUBLIC_BASE_URL}/nowpayments/webhook",
        )
    except httpx.HTTPError:
        logger.exception("Failed to create NOWPayments invoice for %s", order_id)
        await query.edit_message_text(
            _text(content.CARD_INVOICE_FAILED_TEXT, region),
            reply_markup=main_menu(region),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    save_invoice(
        order_id,
        {
            "chat_id": update.effective_chat.id,
            "user_id": user.id,
            "username": user.username,
            # No name is collected for card payments (same as USDT) - fall back to the
            # Telegram display name for the receipt, mirroring handlers/payment.py.
            "name": user.full_name,
            "product_code": product_code,
            "product_name": product["name"],
            "duration_code": duration_code,
            "plan_name": plan_name,
            "price": price,
            "region": region,
            "processed": False,
        },
    )

    text = _text(content.CARD_INVOICE_CREATED_TEXT, region).format(
        product_name=product["name"], plan_name=plan_name, price=price
    )
    await query.edit_message_text(
        text,
        reply_markup=card_invoice_keyboard(invoice["invoice_url"], region),
        parse_mode=ParseMode.MARKDOWN,
    )
