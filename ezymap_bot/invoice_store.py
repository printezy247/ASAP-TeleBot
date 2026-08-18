"""Tiny JSON-file-backed store mapping a NOWPayments invoice's order_id to the Telegram
chat/product/plan it belongs to, so the webhook (a separate request/process) can look up
who to notify when payment succeeds.
"""

import json
import os
from typing import Optional

from .config import NOWPAYMENTS_INVOICE_STORE_FILE


def _load() -> dict:
    if not os.path.exists(NOWPAYMENTS_INVOICE_STORE_FILE):
        return {}
    with open(NOWPAYMENTS_INVOICE_STORE_FILE, "r") as f:
        return json.load(f)


def _save(data: dict) -> None:
    with open(NOWPAYMENTS_INVOICE_STORE_FILE, "w") as f:
        json.dump(data, f)


def save_invoice(order_id: str, record: dict) -> None:
    data = _load()
    data[order_id] = record
    _save(data)


def get_invoice(order_id: str) -> Optional[dict]:
    return _load().get(order_id)


def mark_processed(order_id: str) -> None:
    data = _load()
    if order_id in data:
        data[order_id]["processed"] = True
        _save(data)
