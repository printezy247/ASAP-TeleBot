import logging

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)

from . import content
from .config import BOT_TOKEN, PERSISTENCE_FILE
from .handlers.currency import (
    ASK_CURRENCY_CODE,
    cancel_currency_code,
    currency_selected,
    prompt_currency_code,
    receive_currency_code,
)
from .handlers.currency import restart_via_start as currency_restart_via_start
from .handlers.decision import handle_decision, noop_callback
from .handlers.menu import menu_router
from .handlers.nowpayments_payment import initiate_card_payment
from .handlers.payment import ASK_PROOF
from .handlers.payment import back_to_main_menu as payment_back_to_main_menu
from .handlers.payment import cancel as payment_cancel
from .handlers.payment import plan_selected, receive_proof
from .handlers.payment import restart_via_start as payment_restart_via_start
from .handlers.registration import (
    ASK_ACCOUNT,
    ASK_DEPOSIT_PROOF,
    ASK_EMAIL,
    ASK_NAME,
    cancel,
    receive_account,
    receive_deposit_proof,
    receive_email,
    receive_name,
    restart_via_start,
    submit_start,
)
from .handlers.start import start
from .handlers.stats import stats_command

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def log_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Unhandled exception while processing update %s", update, exc_info=context.error)


def build_application() -> Application:
    persistence = PicklePersistence(filepath=PERSISTENCE_FILE)
    application = Application.builder().token(BOT_TOKEN).persistence(persistence).build()

    registration_conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(submit_start, pattern="^reg_submit$")],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)],
            ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_email)],
            ASK_ACCOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_account)],
            ASK_DEPOSIT_PROOF: [
                MessageHandler(
                    (filters.PHOTO | filters.TEXT) & ~filters.COMMAND, receive_deposit_proof
                )
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("start", restart_via_start),
        ],
        allow_reentry=True,
        name="registration_conversation",
        persistent=True,
    )

    currency_code_conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(prompt_currency_code, pattern="^currency_other$")],
        states={
            ASK_CURRENCY_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_currency_code)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_currency_code),
            CommandHandler("start", currency_restart_via_start),
        ],
        allow_reentry=True,
        name="currency_code_conversation",
        persistent=True,
    )

    payment_conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(plan_selected, pattern="^buy_")],
        states={
            ASK_PROOF: [
                CallbackQueryHandler(payment_back_to_main_menu, pattern="^menu_main$"),
                MessageHandler(
                    (filters.PHOTO | filters.TEXT) & ~filters.COMMAND, receive_proof
                ),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", payment_cancel),
            CommandHandler("start", payment_restart_via_start),
        ],
        allow_reentry=True,
        name="payment_conversation",
        persistent=True,
    )

    quick_pick_codes = "|".join(code for code, _ in content.CURRENCY_QUICK_PICKS)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(registration_conversation)
    application.add_handler(payment_conversation)
    application.add_handler(currency_code_conversation)
    application.add_handler(CallbackQueryHandler(currency_selected, pattern=f"^currency_({quick_pick_codes})$"))
    application.add_handler(CallbackQueryHandler(handle_decision, pattern="^(approve|reject):"))
    application.add_handler(CallbackQueryHandler(noop_callback, pattern="^noop$"))
    application.add_handler(CallbackQueryHandler(initiate_card_payment, pattern="^card_"))
    application.add_handler(CallbackQueryHandler(menu_router))
    application.add_error_handler(log_error)

    return application


def main() -> None:
    application = build_application()
    application.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
