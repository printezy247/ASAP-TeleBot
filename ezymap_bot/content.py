CHANNEL_NAME = "EzyMap Algo"
AMBASSADOR_NAME = "Jack"
BROKER_NAME = "Vantage Markets"
IB_NUMBER = "26468008"
OPEN_ACCOUNT_LINK = "https://vigco.co/la-scom-inv/ms/oQQlQ8yM"
BROKER_WEBSITE = "https://www.vantagemarketsea.com/ms/?affid=MjY0NjgwMDg=&invitecode=oQQlQ8yM"

CHANGE_IB_EMAIL_TO = "lucy.my@vantagemarkets.com"
CHANGE_IB_EMAIL_CC = "shamir.my@vantagemarkets.com"

USDT_WALLET_ADDRESS = "TH2uvMPSj6GJBduK12xKZzM3e8Zg4LeXjA"
USDT_NETWORK = "TRC20"

PLAN_DURATIONS = ["1m", "6m", "1y"]
PLAN_DURATION_LABELS = {"1m": "1 Month", "6m": "6 Months", "1y": "1 Year"}

# code -> {name, description, plans: {duration_code: (price, original_price_or_None)}}
PRODUCTS = {
    "tv_pro": {
        "name": "TradingView - EzyMap Pro",
        "description": "Full EzyMap Pro indicator on TradingView with live signals M1–H4.",
        "plans": {"1m": ("29", None), "6m": ("149", None), "1y": ("249", None)},
    },
    "mt5_bundle": {
        "name": "MT5 Indicator Bundle (Worth $999)",
        "description": "Complete 17 MT5 EzyMap Indicators.",
        "plans": {
            "1m": ("99", "999"),
            "6m": ("499", "5994"),
            "1y": ("999", "11988"),
        },
    },
    "mt5_bulk_close": {
        "name": "Bulk Close – BONUS Layer Close (Top Selling)",
        "description": "Can close partial profit, number of layers with fast executions.",
        "plans": {"1m": ("19", None), "6m": ("109", None), "1y": ("199", None)},
    },
    "mt5_drawdown_guardian": {
        "name": "Drawdown Guardian (Prop Firm Favorite)",
        "description": (
            "Stay alert with your current drawdown to avoid elimination from any prop "
            "firm stages."
        ),
        "plans": {"1m": ("9", None), "6m": ("49", None), "1y": ("99", None)},
    },
    "mt5_auto_tpsl": {
        "name": "Auto TPSL (Trending This Month)",
        "description": "Don't waste your time setting TP & SL manually for each layer.",
        "plans": {"1m": ("9", None), "6m": ("49", None), "1y": ("99", None)},
    },
    "mt5_currency_strength": {
        "name": "Currency Strength Meter",
        "description": (
            "Keep updated with the current volatility of all currencies that are mostly "
            "traded."
        ),
        "plans": {"1m": ("9", None), "6m": ("49", None), "1y": ("99", None)},
    },
    "mt5_mtf_bias": {
        "name": "MTF Bias",
        "description": (
            "Reveal bullish or bearish bias to give confluence for your ever-adapting "
            "trading plan."
        ),
        "plans": {"1m": ("9", None), "6m": ("49", None), "1y": ("99", None)},
    },
}

MT5_BUNDLE_PRODUCT_CODES = [
    "mt5_bundle",
    "mt5_bulk_close",
    "mt5_drawdown_guardian",
    "mt5_auto_tpsl",
    "mt5_currency_strength",
    "mt5_mtf_bias",
]

WELCOME_MESSAGES = [
    (
        "Hey there my trading fam 😎\n\n"
        "I'm excited as you are, just click the button below to start and you'll get your "
        "perks right away !"
    ),
    (
        "Quick reminder before we begin ⚠️\n\n"
        "Trading involves risk. Only trade with capital you're prepared to risk, and treat "
        "any indicators as tools to support decisions, not guarantees."
    ),
    (
        f"My name's {AMBASSADOR_NAME} and I've used {BROKER_NAME} ✅ for years due to its "
        "fast withdrawals and lightning executions for faster entry and exit."
    ),
]

MAIN_MENU_TEXT = "What would you like to do?"

BROKER_INFO_TEXT = (
    f"📘 *Why Choose {BROKER_NAME}*\n\n"
    f"We partner with {BROKER_NAME} for trading. You can check them out directly here:\n"
    f"{BROKER_WEBSITE}"
)

PACKAGES_INTRO_TEXT = (
    f"🎁 *{CHANNEL_NAME} FREE Steps*\n\n"
    f"Everything is unlocked by having a trading account under my IB (`{IB_NUMBER}`) with "
    f"{BROKER_NAME}. The more you have with them, the more you unlock — no extra payment "
    f"needed for these.\n\n"
    "Pick a package to see what it includes:"
)

# key -> (display name, detail text). Keys match the "tier_<key>" callback_data used
# in keyboards.PACKAGE_TIER_MENU, and are stored in context.user_data so the admin
# notification can show which package the client picked.
PACKAGE_TIERS = {
    "beginner": (
        "Beginner",
        (
            "🥉 *Beginner Package*\n\n"
            f"Requirement: open an account under my IB (`{IB_NUMBER}`) — no deposit needed.\n\n"
            "You get:\n"
            "• Free eBooks: Technical Analysis & Mapping Like A Pro\n"
            "• EzyMap Lite indicator (TradingView)"
        ),
    ),
    "pro": (
        "Pro",
        (
            "🥈 *Pro Package*\n\n"
            f"Requirement: open an account under my IB (`{IB_NUMBER}`) + deposit (any amount).\n\n"
            "You get:\n"
            "• EzyMap Scalp Mastery — scalping gold signals channel\n"
            "• Everything in Beginner"
        ),
    ),
    "premium": (
        "Premium",
        (
            "🥇 *Premium Package*\n\n"
            f"Requirement: open an account under my IB (`{IB_NUMBER}`) + deposit min $100.\n\n"
            "You get:\n"
            "• EzyMap Pro indicator (TradingView) with live signals M1–H4\n"
            "• Everything in Pro"
        ),
    ),
    "elite": (
        "Elite",
        (
            "🏆 *Elite Package*\n\n"
            f"Requirement: open an account under my IB (`{IB_NUMBER}`) + deposit min $700.\n\n"
            "You get:\n"
            "• Free eBooks: Technical Analysis & Mapping Like A Pro\n"
            "• EzyMap Scalp Mastery — scalping gold signals channel\n"
            "• EzyMap Pro indicator (TradingView) with live signals\n"
            "• EzyMap indicator for MT5 — Drawdown Guardian, Bulk Close with Layer Close "
            "Function, Auto TPSL, and 5 more (worth $249)\n"
            "• Elite group — 1-on-1 support from Jack (private Telegram group)"
        ),
    ),
}

OPEN_ACCOUNT_TEXT = (
    "💠 *Open a New Account*\n\n"
    f"1️⃣ Click this link to open your account under my IB: {OPEN_ACCOUNT_LINK}\n"
    "2️⃣ Complete the sign-up form with your real details.\n"
    "3️⃣ Verify your email and identity as prompted by "
    f"{BROKER_NAME} — be honest, you'll need this to withdraw later.\n\n"
    "Once your account is open (and deposited, if you're going for Pro/Premium), tap "
    "*✅ I've Completed Registration* below to send me your details."
)

CHANGE_IB_TEXT = (
    "🔁 *Change IB* (only for those who already have a Vantage Markets account)\n\n"
    "This one's done by email, not a link. Send an email with these exact details:\n\n"
    f"To: `{CHANGE_IB_EMAIL_TO}`\n"
    f"Cc: `{CHANGE_IB_EMAIL_CC}`\n"
    "Subject: `Account reassign`\n\n"
    "Body:\n"
    "```\n"
    "Hi,\n\n"
    f"Kindly assist to reassign my account under ({IB_NUMBER}) as he is helping me on my "
    "account.\n\n"
    "Email client: *your registered email* ✅\n\n"
    "Thank you\n"
    "```\n\n"
    "Replace *your registered email* with the email your Vantage account is registered "
    "under, then send it. Once done, tap *✅ I've Completed Registration* below."
)

SUBMIT_DETAILS_PROMPT = (
    "✅ Great — let's get your details sent over so Jack can check your account and unlock "
    "your package.\n\n"
    "What's your *full name*?"
)
ASK_EMAIL_TEXT = "Got it. What's the *email* you registered with?"
ASK_ACCOUNT_TEXT = "Thanks. What's your *account number*?"

SUBMISSION_CONFIRMATION_TEXT = (
    "🎉 Thanks! Your details have been sent to Jack for review.\n\n"
    "Your package perks will be unlocked shortly based on your account status. If you have "
    "questions in the meantime, check the FAQ from the main menu."
)
SUBMISSION_ADMIN_UNREACHABLE_TEXT = (
    "🎉 Thanks, I've got your details!\n\n"
    "I couldn't reach Jack automatically just now, but your submission was recorded — please "
    "also message the admin directly to be safe. Your perks will be unlocked shortly."
)

CANCEL_TEXT = "Cancelled. Use /start any time to open the menu again."

PURCHASE_INTRO_TEXT = (
    "💎 *Purchase EzyMap*\n\n"
    "These are paid, separate from your broker account. Pick a category:"
)

MT5_BUNDLES_INTRO_TEXT = (
    "🖥 *MT5 - EzyMap Bundles*\n\n"
    "Pick an indicator (or the full bundle) to see pricing:"
)


def product_detail_text(product_code: str) -> str:
    product = PRODUCTS[product_code]
    lines = [f"💎 *{product['name']}*", "", product["description"], "", "Pick a plan:"]
    return "\n".join(lines)


def plan_button_label(product_code: str, duration_code: str) -> str:
    price, original_price = PRODUCTS[product_code]["plans"][duration_code]
    duration_label = PLAN_DURATION_LABELS[duration_code]
    if original_price:
        return f"{duration_label} — ${original_price} → ${price}"
    return f"{duration_label} — ${price}"


PAYMENT_PROMPT_TEMPLATE = (
    "💎 *{product_name} — {plan_name}*\n"
    "Price: *${price} USD*\n\n"
    "Send exactly *{price} USDT* ({network} network) to:\n"
    f"`{USDT_WALLET_ADDRESS}`\n\n"
    "⚠️ Send USDT only, on the *{network}* network — wrong coin or wrong network can lose "
    "your funds.\n\n"
    "Once sent, reply here with a *screenshot of the transfer* or your *transaction ID*, and "
    "Jack will confirm and activate your purchase.\n\n"
    "Prefer a different way to pay? Tap the button below to message Jack directly."
)

PAYMENT_PROOF_RECEIVED_TEXT = (
    "✅ Got it! Your payment proof has been sent to Jack.\n\n"
    "He'll confirm and activate your purchase shortly. If you have questions in the "
    "meantime, check the FAQ from the main menu."
)
PAYMENT_PROOF_ADMIN_UNREACHABLE_TEXT = (
    "✅ Got your payment proof!\n\n"
    "I couldn't reach Jack automatically just now — please also message the admin directly "
    "with your proof to be safe. Your purchase will be activated shortly after."
)

FAQ_ITEMS = [
    (
        "Is joining EzyMap Algo free?",
        "Yes — Beginner, Pro, and Premium packages are all unlocked just by having an "
        f"account under my IB with {BROKER_NAME}. Only EzyMap Pro (the paid subscription) "
        "costs money.",
        False,
    ),
    (
        "What's the difference between the free packages and EzyMap Pro?",
        "The free packages (Beginner/Pro/Premium) are unlocked by your broker account status "
        "under my IB. EzyMap Pro is a separate paid subscription with the full indicator and "
        "live signals from M1 to H4.",
        False,
    ),
    (
        "How much do I need to deposit?",
        "Beginner needs no deposit. Pro needs any deposit amount. Premium needs a minimum "
        "$100 deposit. All under my IB.",
        False,
    ),
    (
        "I already have a Vantage account. Can I still join?",
        "Yes — use *Change IB* instead of opening a new account (it's done by email, not a "
        "link), then submit your details the same way.",
        False,
    ),
    (
        "How long until my package is unlocked?",
        "Once you submit your Name, Email, and Account Number, Jack checks your account "
        "status and unlocks the matching package shortly after — usually the same day.",
        False,
    ),
    (
        "How do I pay for a paid indicator or bundle?",
        "Tap *💎 Purchase EzyMap* from the main menu, pick TradingView or MT5, then a plan "
        "— you'll get a USDT wallet address plus instructions to confirm with Jack (or a "
        "button to ask him about a different payment method).",
        False,
    ),
    (
        "Can I cancel or get a refund on a paid indicator/bundle?",
        "Message Jack directly to discuss — refund/cancellation isn't handled automatically "
        "through the bot.",
        True,
    ),
    (
        "Do I need TradingView for the indicators?",
        "Yes, EzyMap Lite/Scalp Mastery/Pro are TradingView indicators — you'll need a free "
        "or paid TradingView account to use them.",
        False,
    ),
    (
        "What if I get stuck during registration or payment?",
        "Go through the Open Account or Change IB steps again from the menu, or tap the "
        "button below to message Jack directly.",
        True,
    ),
]
