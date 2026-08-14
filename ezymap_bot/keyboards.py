from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .config import ADMIN_CHAT_ID

# TODO: if Jack gets a public @username, swap this for f"https://t.me/{username}" —
# it's more reliable than tg://user?id=, which depends on the viewer's privacy settings.
ADMIN_CONTACT_URL = f"tg://user?id={ADMIN_CHAT_ID}"

LANGUAGE_SELECT_MENU = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇲🇾 Bahasa Melayu", callback_data="lang_my")],
    ]
)

MAIN_MENU = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🎁 Check Out FREE Steps", callback_data="menu_packages")],
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


PURCHASE_CATEGORY_MENU = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("📈 TradingView - EzyMap Pro (best seller)", callback_data="product_tv_pro")],
        [InlineKeyboardButton("🖥 MT5 - EzyMap Bundles", callback_data="products_mt5")],
        [InlineKeyboardButton("⬅️ Main Menu", callback_data="menu_main")],
    ]
)

BACK_TO_PURCHASE = InlineKeyboardMarkup(
    [[InlineKeyboardButton("⬅️ Back", callback_data="menu_pro")]]
)


def mt5_bundles_menu() -> InlineKeyboardMarkup:
    from .content import MT5_BUNDLE_PRODUCT_CODES, PRODUCTS

    rows = [
        [InlineKeyboardButton(PRODUCTS[code]["name"], callback_data=f"product_{code}")]
        for code in MT5_BUNDLE_PRODUCT_CODES
    ]
    rows.append([InlineKeyboardButton("⬅️ Back", callback_data="menu_pro")])
    rows.append([InlineKeyboardButton("⬅️ Main Menu", callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)


def product_detail_menu(product_code: str, region: str) -> InlineKeyboardMarkup:
    from .content import DEFAULT_PRICE_REGION, MT5_BUNDLE_PRODUCT_CODES, PLAN_DURATIONS, TRADINGVIEW_FREE_URL, plan_button_label

    region = region or DEFAULT_PRICE_REGION
    rows = [
        [
            InlineKeyboardButton(
                plan_button_label(product_code, duration, region),
                callback_data=f"choose_pay_{product_code}_{duration}",
            )
        ]
        for duration in PLAN_DURATIONS
    ]
    if product_code == "tv_pro":
        rows.append([InlineKeyboardButton("📊 Get TradingView FREE", url=TRADINGVIEW_FREE_URL)])
    back_target = "products_mt5" if product_code in MT5_BUNDLE_PRODUCT_CODES else "menu_pro"
    rows.append([InlineKeyboardButton("⬅️ Back", callback_data=back_target)])
    rows.append([InlineKeyboardButton("⬅️ Main Menu", callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)


def payment_method_menu(product_code: str, duration: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💰 Pay with USDT", callback_data=f"buy_{product_code}_{duration}")],
            [
                InlineKeyboardButton(
                    "💳 Pay with Card/Bank/E-Wallet", callback_data=f"xendit_{product_code}_{duration}"
                )
            ],
            [InlineKeyboardButton("⬅️ Main Menu", callback_data="menu_main")],
        ]
    )


DIFFERENT_PAYMENT_METHOD_URL = "https://t.me/m/Z-yb3fL4NWVl"


def payment_prompt_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "💬 I want different payment method", url=DIFFERENT_PAYMENT_METHOD_URL
                )
            ],
            [InlineKeyboardButton("⬅️ Main Menu", callback_data="menu_main")],
        ]
    )


# Same layout as payment_prompt_keyboard, used on Xendit unavailable/failed screens.
different_payment_method_keyboard = payment_prompt_keyboard


def xendit_invoice_keyboard(invoice_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔗 Pay Now", url=invoice_url)],
            [InlineKeyboardButton("⬅️ Main Menu", callback_data="menu_main")],
        ]
    )


def faq_menu() -> InlineKeyboardMarkup:
    from .content import FAQ_ITEMS

    rows = [
        [InlineKeyboardButton(question, callback_data=f"faq_{i}")]
        for i, (question, _answer, _show_contact_admin, _extra_button) in enumerate(FAQ_ITEMS)
    ]
    rows.append([InlineKeyboardButton("⬅️ Main Menu", callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)


def faq_answer_keyboard(show_contact_admin: bool, extra_button=None) -> InlineKeyboardMarkup:
    rows = []
    if extra_button:
        label, url = extra_button
        rows.append([InlineKeyboardButton(label, url=url)])
    if show_contact_admin:
        rows.append([InlineKeyboardButton("📞 Contact Admin", url=ADMIN_CONTACT_URL)])
    rows.append([InlineKeyboardButton("⬅️ Back to FAQ", callback_data="menu_faq")])
    return InlineKeyboardMarkup(rows)
