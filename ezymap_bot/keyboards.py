from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .config import ADMIN_CHAT_ID

# TODO: if Jack gets a public @username, swap this for f"https://t.me/{username}" —
# it's more reliable than tg://user?id=, which depends on the viewer's privacy settings.
ADMIN_CONTACT_URL = f"tg://user?id={ADMIN_CHAT_ID}"

MAIN_MENU = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🎁 See Packages", callback_data="menu_packages")],
        [InlineKeyboardButton("💎 Purchase EzyMap", callback_data="menu_pro")],
        [InlineKeyboardButton("📘 Why Choose Vantage", callback_data="menu_broker")],
        [InlineKeyboardButton("❓ FAQ", callback_data="menu_faq")],
    ]
)

BACK_TO_MAIN = InlineKeyboardMarkup(
    [[InlineKeyboardButton("⬅️ Main Menu", callback_data="menu_main")]]
)

PACKAGE_TIER_MENU = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🥉 Beginner", callback_data="tier_beginner")],
        [InlineKeyboardButton("🥈 Pro", callback_data="tier_pro")],
        [InlineKeyboardButton("🥇 Premium", callback_data="tier_premium")],
        [InlineKeyboardButton("🏆 Elite", callback_data="tier_elite")],
        [InlineKeyboardButton("⬅️ Main Menu", callback_data="menu_main")],
    ]
)

TIER_DETAIL_MENU = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🆕 Open New Account", callback_data="reg_open_account")],
        [InlineKeyboardButton("🔁 Change IB", callback_data="reg_change_ib")],
        [InlineKeyboardButton("✅ I've Completed Registration", callback_data="reg_submit")],
        [InlineKeyboardButton("⬅️ Back to Packages", callback_data="menu_packages")],
        [InlineKeyboardButton("⬅️ Main Menu", callback_data="menu_main")],
    ]
)

BACK_TO_PACKAGES = InlineKeyboardMarkup(
    [[InlineKeyboardButton("⬅️ Back", callback_data="menu_packages")]]
)


def ezymap_pro_plans_menu() -> InlineKeyboardMarkup:
    from .content import EZYMAP_PRO_PLANS

    rows = [
        [InlineKeyboardButton(f"{name} — ${price}", callback_data=f"pay_{code}")]
        for name, price, code in EZYMAP_PRO_PLANS
    ]
    rows.append([InlineKeyboardButton("⬅️ Main Menu", callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)


def faq_menu() -> InlineKeyboardMarkup:
    from .content import FAQ_ITEMS

    rows = [
        [InlineKeyboardButton(question, callback_data=f"faq_{i}")]
        for i, (question, _answer, _show_contact_admin) in enumerate(FAQ_ITEMS)
    ]
    rows.append([InlineKeyboardButton("⬅️ Main Menu", callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)


def faq_answer_keyboard(show_contact_admin: bool) -> InlineKeyboardMarkup:
    rows = []
    if show_contact_admin:
        rows.append([InlineKeyboardButton("📞 Contact Admin", url=ADMIN_CONTACT_URL)])
    rows.append([InlineKeyboardButton("⬅️ Back to FAQ", callback_data="menu_faq")])
    return InlineKeyboardMarkup(rows)
