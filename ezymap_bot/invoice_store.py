"""Tiny JSON-file-backed store mapping a Xendit invoice's external_id to the Telegram
chat/product/plan it belongs to, so the webhook (a separate request/process) can look
up who to notify when payment succeeds.
"""

import json
import os
from typing import Optional

from .config import INVOICE_STORE_FILE


def _load() -> dict:
    if not os.path.exists(INVOICE_STORE_FILE):
        return {}
    with open(INVOICE_STORE_FILE, "r") as f:
        return json.load(f)


def _save(data: dict) -> None:
    with open(INVOICE_STORE_FILE, "w") as f:
        json.dump(data, f)


def save_invoice(external_id: str, record: dict) -> None:
    data = _load()
    data[external_id] = record
    _save(data)


def get_invoice(external_id: str) -> Optional[dict]:
    return _load().get(external_id)


def mark_processed(external_id: str) -> None:
    data = _load()
    if external_id in data:
        data[external_id]["processed"] = True
        _save(data)
