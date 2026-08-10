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

from .config import BOT_TOKEN, PERSISTENCE_FILE
from .handlers.menu import menu_router
from .handlers.payment import ASK_PROOF
from .handlers.payment import cancel as payment_cancel
from .handlers.payment import plan_selected, receive_proof
from .handlers.payment import restart_via_start as payment_restart_via_start
from .handlers.registration import (
    ASK_ACCOUNT,
    ASK_EMAIL,
    ASK_NAME,
    cancel,
    receive_account,
    receive_email,
    receive_name,
    restart_via_start,
    submit_start,
)
from .handlers.start import start

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
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("start", restart_via_start),
        ],
        allow_reentry=True,
        name="registration_conversation",
        persistent=True,
    )

    payment_conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(plan_selected, pattern="^pay_plan_")],
        states={
            ASK_PROOF: [
                MessageHandler(
                    (filters.PHOTO | filters.TEXT) & ~filters.COMMAND, receive_proof
                )
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

    application.add_handler(CommandHandler("start", start))
    application.add_handler(registration_conversation)
    application.add_handler(payment_conversation)
    application.add_handler(CallbackQueryHandler(menu_router))
    application.add_error_handler(log_error)

    return application


def main() -> None:
    application = build_application()
    application.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
