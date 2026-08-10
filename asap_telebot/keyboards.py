from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .config import ADMIN_CHAT_ID

MAIN_MENU = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🚦 Get My Free Signals", callback_data="menu_signals")],
        [InlineKeyboardButton("📘 Learn More About Broker", callback_data="menu_broker")],
        [InlineKeyboardButton("❓ FAQ", callback_data="menu_faq")],
    ]
)

BACK_TO_MAIN = InlineKeyboardMarkup(
    [[InlineKeyboardButton("⬅️ Main Menu", callback_data="menu_main")]]
)

SIGNALS_MENU = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🆕 Open New Account", callback_data="reg_open_account")],
        [InlineKeyboardButton("🔁 Change IB", callback_data="reg_change_ib")],
        [InlineKeyboardButton("💰 Deposit", callback_data="reg_deposit")],
        [InlineKeyboardButton("💸 Withdraw", callback_data="reg_withdraw")],
        [InlineKeyboardButton("✅ I've Completed Registration", callback_data="reg_submit")],
        [InlineKeyboardButton("⬅️ Main Menu", callback_data="menu_main")],
    ]
)

BACK_TO_SIGNALS = InlineKeyboardMarkup(
    [[InlineKeyboardButton("⬅️ Back", callback_data="menu_signals")]]
)

DEPOSIT_MENU = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🏦 Local Bank", callback_data="deposit_bank")],
        [InlineKeyboardButton("💳 Card / E-Wallet", callback_data="deposit_card")],
        [InlineKeyboardButton("₿ Bitcoin (BTC)", callback_data="deposit_btc")],
        [InlineKeyboardButton("🟢 Tether (USDT)", callback_data="deposit_usdt")],
        [InlineKeyboardButton("⬅️ Back", callback_data="menu_signals")],
    ]
)

BACK_TO_DEPOSIT = InlineKeyboardMarkup(
    [[InlineKeyboardButton("⬅️ Back", callback_data="reg_deposit")]]
)


def faq_menu() -> InlineKeyboardMarkup:
    from .content import FAQ_ITEMS

    rows = [
        [InlineKeyboardButton(question, callback_data=f"faq_{i}")]
        for i, (question, _answer) in enumerate(FAQ_ITEMS)
    ]
    rows.append([InlineKeyboardButton("⬅️ Main Menu", callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)


BACK_TO_FAQ = InlineKeyboardMarkup(
    [[InlineKeyboardButton("⬅️ Back to FAQ", callback_data="menu_faq")]]
)


def faq_answer_keyboard(show_contact_admin: bool) -> InlineKeyboardMarkup:
    rows = []
    if show_contact_admin:
        rows.append(
            [InlineKeyboardButton("📞 Contact Admin", url=f"tg://user?id={ADMIN_CHAT_ID}")]
        )
    rows.append([InlineKeyboardButton("⬅️ Back to FAQ", callback_data="menu_faq")])
    return InlineKeyboardMarkup(rows)
