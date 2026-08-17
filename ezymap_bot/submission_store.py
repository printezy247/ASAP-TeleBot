"""Tracks pending registration/USDT-payment submissions awaiting an admin
approve/reject tap, keyed by a short random id (kept out of callback_data
directly since Telegram caps that at 64 bytes). Stored in bot_data so it
survives a restart via the same PicklePersistence file everything else uses.
"""

import secrets

_KEY = "pending_submissions"


def create_submission(context, data: dict) -> str:
    submission_id = secrets.token_hex(5)
    context.bot_data.setdefault(_KEY, {})[submission_id] = data
    return submission_id


def get_submission(context, submission_id: str):
    return context.bot_data.get(_KEY, {}).get(submission_id)


def remove_submission(context, submission_id: str) -> None:
    context.bot_data.get(_KEY, {}).pop(submission_id, None)
