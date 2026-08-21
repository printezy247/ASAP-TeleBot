from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .config import ADMIN_CHAT_ID
from .content import DEFAULT_PRICE_REGION

# TODO: if Jack gets a public @username, swap this for f"https://t.me/{username}" —
# it's more reliable than tg://user?id=, which depends on the viewer's privacy settings.
ADMIN_CONTACT_URL = f"tg://user?id={ADMIN_CHAT_ID}"

DIFFERENT_PAYMENT_METHOD_URL = "https://t.me/m/Z-yb3fL4NWVl"

FREE_CHANNEL_URL = "https://t.me/ezymap"

# Button chrome shared across screens. Product/brand names (EzyMap, TradingView, MT5,
# Vantage, USDT, tier names Beginner/Pro/Premium/Elite) stay in English in both
# languages - only the surrounding action words are translated.
_LABELS = {
    "main_menu": {"en": "⬅️ Main Menu", "my": "⬅️ Menu Utama"},
    "back": {"en": "⬅️ Back", "my": "⬅️ Kembali"},
    "back_to_packages": {"en": "⬅️ Back to Packages", "my": "⬅️ Kembali ke Pakej"},
    "back_to_faq": {"en": "⬅️ Back to FAQ", "my": "⬅️ Kembali ke FAQ"},
    "check_out_free_steps": {"en": "🎁 Check Out FREE Steps", "my": "🎁 Lihat Langkah PERCUMA"},
    "purchase_ezymap": {"en": "💎 Purchase EzyMap", "my": "💎 Beli EzyMap"},
    "why_choose_vantage": {"en": "📘 Why Choose Vantage", "my": "📘 Kenapa Pilih Vantage"},
    "faq": {"en": "❓ FAQ", "my": "❓ Soalan Lazim"},
    "open_new_account": {"en": "🆕 Open New Account", "my": "🆕 Buka Akaun Baharu"},
    "change_ib": {"en": "🔁 Change IB", "my": "🔁 Tukar IB"},
    "completed_registration": {
        "en": "✅ I've Completed Registration",
        "my": "✅ Saya Telah Selesai Daftar",
    },
    "tv_pro_category": {
        "en": "📈 TradingView - EzyMap Pro (best seller)",
        "my": "📈 TradingView - EzyMap Pro (paling laris)",
    },
    "mt5_bundles_category": {"en": "🖥 MT5 - EzyMap Bundles", "my": "🖥 MT5 - EzyMap Bundles"},
    "pay_usdt": {"en": "💰 Pay with USDT", "my": "💰 Bayar dengan USDT"},
    "pay_card": {"en": "💳 Pay by Card", "my": "💳 Bayar dengan Kad"},
    "open_invoice": {"en": "💳 Pay Now", "my": "💳 Bayar Sekarang"},
    "different_payment_method": {
        "en": "💬 I want different payment method",
        "my": "💬 Saya mahu cara bayaran lain",
    },
    "contact_admin": {"en": "📞 Contact Admin", "my": "📞 Hubungi Admin"},
    "free_channel": {"en": "📢 Join Our Free Channel", "my": "📢 Join Channel Percuma Kami"},
}


def _label(key: str, region: str) -> str:
    return _LABELS[key].get(region, _LABELS[key][DEFAULT_PRICE_REGION])


# Language (content wording) and currency (price display) are two separate steps -
# language stays just English/Bahasa Melayu, but currency shouldn't be tied to it,
# since clients anywhere in the world can speak either and still want their own
# local currency. See currency_select_menu() below for that second step.
LANGUAGE_SELECT_MENU = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇲🇾 Bahasa Melayu", callback_data="lang_my")],
    ]
)


def currency_select_menu(region: str) -> InlineKeyboardMarkup:
    from .content import CURRENCY_QUICK_PICKS

    rows = [[InlineKeyboardButton(label, callback_data=f"currency_{code}")] for code, label in CURRENCY_QUICK_PICKS]
    other_label = "🌐 Kod Lain" if region == "my" else "🌐 Other Currency"
    rows.append([InlineKeyboardButton(other_label, callback_data="currency_other")])
    return InlineKeyboardMarkup(rows)


def main_menu(region: str) -> InlineKeyboardMarkup:
    # Why Choose Vantage lives on the package_tier_menu screen instead (reached via
    # Check Out FREE Steps) - keeps the very first thing a client sees to the 3
    # things that actually matter for conversion, plus FAQ as a safety net.
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(_label("check_out_free_steps", region), callback_data="menu_packages")],
            [InlineKeyboardButton(_label("purchase_ezymap", region), callback_data="menu_pro")],
            [InlineKeyboardButton(_label("faq", region), callback_data="menu_faq")],
            [InlineKeyboardButton(_label("free_channel", region), url=FREE_CHANNEL_URL)],
        ]
    )


def back_to_main(region: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(_label("main_menu", region), callback_data="menu_main")]])


def package_tier_menu(region: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🥉 Beginner", callback_data="tier_beginner")],
            [InlineKeyboardButton("🥈 Pro", callback_data="tier_pro")],
            [InlineKeyboardButton("🥇 Premium", callback_data="tier_premium")],
            [InlineKeyboardButton("🏆 Elite", callback_data="tier_elite")],
            [InlineKeyboardButton(_label("why_choose_vantage", region), callback_data="menu_broker")],
            [InlineKeyboardButton(_label("main_menu", region), callback_data="menu_main")],
        ]
    )


def tier_detail_menu(region: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(_label("open_new_account", region), callback_data="reg_open_account")],
            [InlineKeyboardButton(_label("change_ib", region), callback_data="reg_change_ib")],
            [InlineKeyboardButton(_label("completed_registration", region), callback_data="reg_submit")],
            [InlineKeyboardButton(_label("back_to_packages", region), callback_data="menu_packages")],
            [InlineKeyboardButton(_label("main_menu", region), callback_data="menu_main")],
        ]
    )


def back_to_packages(region: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(_label("back", region), callback_data="menu_packages")]])


def purchase_category_menu(region: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(_label("tv_pro_category", region), callback_data="product_tv_pro")],
            [InlineKeyboardButton(_label("mt5_bundles_category", region), callback_data="products_mt5")],
            [InlineKeyboardButton(_label("main_menu", region), callback_data="menu_main")],
        ]
    )


def mt5_bundles_menu(region: str) -> InlineKeyboardMarkup:
    from .content import MT5_BUNDLE_PRODUCT_CODES, PRODUCTS

    rows = [
        [InlineKeyboardButton(PRODUCTS[code]["name"], callback_data=f"product_{code}")]
        for code in MT5_BUNDLE_PRODUCT_CODES
    ]
    rows.append([InlineKeyboardButton(_label("back", region), callback_data="menu_pro")])
    rows.append([InlineKeyboardButton(_label("main_menu", region), callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)


def product_detail_menu(product_code: str, region: str, currency: str = None) -> InlineKeyboardMarkup:
    from .content import DEFAULT_CURRENCY, MT5_BUNDLE_PRODUCT_CODES, PLAN_DURATIONS, TRADINGVIEW_FREE_URL, plan_button_label

    region = region or DEFAULT_PRICE_REGION
    currency = currency or DEFAULT_CURRENCY
    rows = [
        [
            InlineKeyboardButton(
                plan_button_label(product_code, duration, region, currency),
                callback_data=f"choose_pay_{product_code}_{duration}",
            )
        ]
        for duration in PLAN_DURATIONS
    ]
    if product_code == "tv_pro":
        label = "📊 Dapatkan TradingView PERCUMA" if region == "my" else "📊 Get TradingView FREE"
        rows.append([InlineKeyboardButton(label, url=TRADINGVIEW_FREE_URL)])
    back_target = "products_mt5" if product_code in MT5_BUNDLE_PRODUCT_CODES else "menu_pro"
    rows.append([InlineKeyboardButton(_label("back", region), callback_data=back_target)])
    rows.append([InlineKeyboardButton(_label("main_menu", region), callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)


def payment_method_menu(product_code: str, duration: str, region: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(_label("pay_usdt", region), callback_data=f"buy_{product_code}_{duration}")],
            [InlineKeyboardButton(_label("pay_card", region), callback_data=f"card_{product_code}_{duration}")],
            [InlineKeyboardButton(_label("main_menu", region), callback_data="menu_main")],
        ]
    )


def card_invoice_keyboard(invoice_url: str, region: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(_label("open_invoice", region), url=invoice_url)],
            [InlineKeyboardButton(_label("main_menu", region), callback_data="menu_main")],
        ]
    )


def payment_prompt_keyboard(region: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(_label("different_payment_method", region), url=DIFFERENT_PAYMENT_METHOD_URL)],
            [InlineKeyboardButton(_label("main_menu", region), callback_data="menu_main")],
        ]
    )


def faq_menu(region: str) -> InlineKeyboardMarkup:
    from .content import DEFAULT_PRICE_REGION as _DEFAULT, FAQ_ITEMS

    rows = [
        [
            InlineKeyboardButton(
                item["question"].get(region, item["question"][_DEFAULT]), callback_data=f"faq_{i}"
            )
        ]
        for i, item in enumerate(FAQ_ITEMS)
    ]
    rows.append([InlineKeyboardButton(_label("main_menu", region), callback_data="menu_main")])
    return InlineKeyboardMarkup(rows)


def faq_answer_keyboard(show_contact_admin: bool, extra_button, region: str) -> InlineKeyboardMarkup:
    rows = []
    if extra_button:
        label = extra_button["label"].get(region, extra_button["label"][DEFAULT_PRICE_REGION])
        rows.append([InlineKeyboardButton(label, url=extra_button["url"])])
    if show_contact_admin:
        rows.append([InlineKeyboardButton(_label("contact_admin", region), url=ADMIN_CONTACT_URL)])
    rows.append([InlineKeyboardButton(_label("back_to_faq", region), callback_data="menu_faq")])
    return InlineKeyboardMarkup(rows)
