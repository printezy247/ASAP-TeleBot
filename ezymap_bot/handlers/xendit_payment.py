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


async def initiate_xendit_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    payload = query.data.removeprefix("xendit_")
    product_code, duration_code = payload.rsplit("_", 1)

    if product_code not in content.PRODUCTS:
        await query.edit_message_text(
            content.MAIN_MENU_TEXT, reply_markup=different_payment_method_keyboard()
        )
        return

    if not XENDIT_SECRET_KEY:
        await query.edit_message_text(
            content.XENDIT_UNAVAILABLE_TEXT,
            reply_markup=different_payment_method_keyboard(),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    product = content.PRODUCTS[product_code]
    price = product["plans"][duration_code]
    plan_name = content.PLAN_DURATION_LABELS[duration_code]
    region = context.user_data.get("price_region", content.DEFAULT_PRICE_REGION)
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
            content.XENDIT_INVOICE_FAILED_TEXT,
            reply_markup=different_payment_method_keyboard(),
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
            "processed": False,
        },
    )

    text = content.XENDIT_INVOICE_CREATED_TEXT.format(
        product_name=product["name"], plan_name=plan_name, price=f"{symbol}{price}"
    )
    await query.edit_message_text(
        text,
        reply_markup=xendit_invoice_keyboard(invoice["invoice_url"]),
        parse_mode=ParseMode.MARKDOWN,
    )
