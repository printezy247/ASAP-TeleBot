import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import ContextTypes

from .. import content
from ..config import ADMIN_CHAT_ID
from ..receipt import generate_receipt_image
from ..submission_store import get_submission, remove_submission

logger = logging.getLogger(__name__)

_DECISION_TEXT = {
    ("registration", True): content.REGISTRATION_APPROVED_TEXT,
    ("registration", False): content.REGISTRATION_REJECTED_TEXT,
    ("payment", True): content.PAYMENT_APPROVED_TEXT,
    ("payment", False): content.PAYMENT_REJECTED_TEXT,
}


def _text(text_dict: dict, region: str) -> str:
    return text_dict.get(region, text_dict[content.DEFAULT_PRICE_REGION])


async def handle_decision(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    # Only the admin's own chat can approve/reject - this button grants access or
    # confirms a payment, so it's worth a cheap extra check beyond "only the admin
    # chat ever receives this message" as a defense against a forwarded/replayed tap.
    if str(update.effective_chat.id) != str(ADMIN_CHAT_ID):
        await query.answer()
        return

    action, _, submission_id = query.data.partition(":")
    submission = get_submission(context, submission_id)
    if submission is None:
        await query.answer("That one's already been handled or expired.", show_alert=True)
        return
    await query.answer()
    remove_submission(context, submission_id)

    approved = action == "approve"
    text_dict = _DECISION_TEXT[(submission["kind"], approved)]
    client_text = _text(text_dict, submission["region"]).format(label=submission["label"])

    try:
        if approved:
            try:
                # Older pending submissions (created before this field existed) may
                # not have a name on file - fall back rather than KeyError on a
                # stale record.
                receipt = generate_receipt_image(
                    kind=submission["kind"],
                    region=submission["region"],
                    name=submission.get("name") or "-",
                    label=submission["label"],
                )
                await context.bot.send_photo(
                    chat_id=submission["chat_id"],
                    photo=receipt,
                    caption=client_text,
                    parse_mode=ParseMode.MARKDOWN,
                )
            except TelegramError:
                raise
            except Exception:
                # Receipt rendering itself failed (bad font path, Pillow error,
                # etc) - the client still needs to hear they were approved, so
                # fall back to the plain-text confirmation instead of going
                # silent. Re-raising TelegramError above keeps genuine delivery
                # failures (chat not found, blocked, ...) handled the normal
                # way below instead of double-sending.
                logger.exception(
                    "Failed to generate/send receipt image for submission %s, "
                    "falling back to plain text",
                    submission_id,
                )
                await context.bot.send_message(
                    chat_id=submission["chat_id"], text=client_text, parse_mode=ParseMode.MARKDOWN
                )
        else:
            await context.bot.send_message(
                chat_id=submission["chat_id"], text=client_text, parse_mode=ParseMode.MARKDOWN
            )
    except TelegramError:
        logger.exception(
            "Failed to notify client (chat_id=%s) of decision for submission %s",
            submission["chat_id"],
            submission_id,
        )

    status_label = "✅ Approved" if approved else "❌ Rejected"
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(status_label, callback_data="noop")]])
        )
    except TelegramError:
        # Non-fatal - the decision was still applied and the client notified.
        pass


async def noop_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
