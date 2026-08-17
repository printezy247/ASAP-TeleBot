import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import ContextTypes, ConversationHandler

from .. import content
from ..config import ADMIN_CHAT_ID
from ..keyboards import main_menu
from ..submission_store import create_submission, remove_submission
from .start import start

logger = logging.getLogger(__name__)

ASK_NAME, ASK_EMAIL, ASK_ACCOUNT, ASK_DEPOSIT_PROOF = range(4)

TIERS_REQUIRING_DEPOSIT_PROOF = {"pro", "premium", "elite"}


def _region(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("price_region", content.DEFAULT_PRICE_REGION)


def _text(text_dict: dict, region: str) -> str:
    return text_dict.get(region, text_dict[content.DEFAULT_PRICE_REGION])


def _clear_reg_data(context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.pop("reg_name", None)
    context.user_data.pop("reg_email", None)
    context.user_data.pop("reg_account", None)


async def submit_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    text = _text(content.SUBMIT_DETAILS_PROMPT, _region(context))
    # The tier detail screen may be a photo message (package tier image) - edit_message_text
    # fails on those, so replace the message instead of editing it in that case.
    if query.message.photo:
        await query.delete_message()
        await query.message.chat.send_message(text, parse_mode=ParseMode.MARKDOWN)
    else:
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN)
    return ASK_NAME


async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["reg_name"] = update.message.text.strip()
    await update.message.reply_text(
        _text(content.ASK_EMAIL_TEXT, _region(context)), parse_mode=ParseMode.MARKDOWN
    )
    return ASK_EMAIL


async def receive_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["reg_email"] = update.message.text.strip()
    await update.message.reply_text(
        _text(content.ASK_ACCOUNT_TEXT, _region(context)), parse_mode=ParseMode.MARKDOWN
    )
    return ASK_ACCOUNT


async def receive_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["reg_account"] = update.message.text.strip()

    tier_key = context.user_data.get("selected_package")
    if tier_key in TIERS_REQUIRING_DEPOSIT_PROOF:
        await update.message.reply_text(
            _text(content.ASK_DEPOSIT_PROOF_TEXT, _region(context)), parse_mode=ParseMode.MARKDOWN
        )
        return ASK_DEPOSIT_PROOF

    return await _finalize_submission(update, context)


async def receive_deposit_proof(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await _finalize_submission(update, context, proof_message=update.message)


async def _finalize_submission(
    update: Update, context: ContextTypes.DEFAULT_TYPE, proof_message=None
) -> int:
    region = _region(context)
    name = context.user_data.get("reg_name", "-")
    email = context.user_data.get("reg_email", "-")
    account = context.user_data.get("reg_account", "-")
    user = update.effective_user

    tier_key = context.user_data.get("selected_package")
    package_line = content.PACKAGE_TIERS[tier_key]["name"] if tier_key in content.PACKAGE_TIERS else "Not specified"

    submission_id = create_submission(
        context,
        {
            "kind": "registration",
            "chat_id": update.effective_chat.id,
            "region": region,
            "label": package_line,
        },
    )

    # Admin-facing notification always stays in English - it's for Jack, not the client.
    username_line = f"@{user.username}" if user.username else "(no username set)"
    proof_note = "\n\nDeposit proof is forwarded below." if proof_message else ""
    admin_text = (
        "📥 *New EzyMap Algo registration submission*\n\n"
        f"Package: {package_line}\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Account Number: {account}\n\n"
        f"Telegram username: {username_line}\n"
        f"Telegram ID: `{user.id}`"
        f"{proof_note}"
    )
    decision_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💬 Chat with Client", url=f"tg://user?id={user.id}")],
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve:{submission_id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject:{submission_id}"),
            ],
        ]
    )

    admin_notified = True
    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=decision_keyboard,
        )
        if proof_message is not None:
            await context.bot.forward_message(
                chat_id=ADMIN_CHAT_ID,
                from_chat_id=update.effective_chat.id,
                message_id=proof_message.message_id,
            )
    except TelegramError:
        admin_notified = False
        remove_submission(context, submission_id)
        logger.exception(
            "Failed to DM admin (chat_id=%s) with registration submission from user %s. "
            "The admin account must send /start to this bot at least once before it can "
            "receive DMs.",
            ADMIN_CHAT_ID,
            user.id,
        )

    confirmation_text = _text(
        content.SUBMISSION_CONFIRMATION_TEXT if admin_notified else content.SUBMISSION_ADMIN_UNREACHABLE_TEXT,
        region,
    )
    await update.message.reply_text(
        confirmation_text,
        reply_markup=main_menu(region),
        parse_mode=ParseMode.MARKDOWN,
    )

    _clear_reg_data(context)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        _text(content.CANCEL_TEXT, _region(context)), reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


async def restart_via_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _clear_reg_data(context)
    await start(update, context)
    return ConversationHandler.END
