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

EZYMAP_PRO_PLANS = [
    ("1 Month", "29", "plan_1m"),
    ("6 Months", "149", "plan_6m"),
    ("1 Year", "249", "plan_1y"),
]

WELCOME_MESSAGES = [
    (
        f"👋 Welcome to *{CHANNEL_NAME}*!\n\n"
        f"I'm your registration assistant — everything below is done with buttons, fast and "
        f"no waiting around for answers."
    ),
    (
        "⚠️ *Quick risk reminder before we begin*\n\n"
        "Trading involves risk. Only trade with capital you're prepared to risk, and treat "
        "any signals or indicators as tools to support your own decisions, not guarantees."
    ),
    (
        f"✅ Let's go! Ambassador: *{AMBASSADOR_NAME}* | Broker: *{BROKER_NAME}*"
    ),
]

MAIN_MENU_TEXT = "What would you like to do?"

BROKER_INFO_TEXT = (
    f"📘 *Why Choose {BROKER_NAME}*\n\n"
    f"We partner with {BROKER_NAME} for trading. You can check them out directly here:\n"
    f"{BROKER_WEBSITE}"
)

PACKAGES_INTRO_TEXT = (
    f"🎁 *{CHANNEL_NAME} Packages*\n\n"
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
            "Function, Auto TPSL, and 2 more (worth $149)\n"
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

EZYMAP_PRO_INTRO_TEXT = (
    "💎 *EzyMap Pro Subscription*\n\n"
    "This is a paid subscription, separate from your broker account — it's the premium "
    "version of the indicator with full live signal coverage.\n\n"
    "Choose a plan:"
)

PAYMENT_PROMPT_TEMPLATE = (
    "💎 *EzyMap Pro — {plan_name}*\n"
    "Price: *${price} USD*\n\n"
    "Send exactly *{price} USDT* ({network} network) to:\n"
    f"`{USDT_WALLET_ADDRESS}`\n\n"
    "⚠️ Send USDT only, on the *{network}* network — wrong coin or wrong network can lose "
    "your funds.\n\n"
    "Once sent, reply here with a *screenshot of the transfer* or your *transaction ID*, and "
    "Jack will confirm and activate your subscription."
)

PAYMENT_PROOF_RECEIVED_TEXT = (
    "✅ Got it! Your payment proof has been sent to Jack.\n\n"
    "He'll confirm and activate your EzyMap Pro subscription shortly. If you have questions "
    "in the meantime, check the FAQ from the main menu."
)
PAYMENT_PROOF_ADMIN_UNREACHABLE_TEXT = (
    "✅ Got your payment proof!\n\n"
    "I couldn't reach Jack automatically just now — please also message the admin directly "
    "with your proof to be safe. Your subscription will be activated shortly after."
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
        "How do I pay for EzyMap Pro?",
        "Tap *💎 Get EzyMap Pro* from the main menu, pick a plan, and you'll get a USDT "
        "wallet address to send payment to, plus instructions to confirm with Jack.",
        False,
    ),
    (
        "Can I cancel or get a refund on EzyMap Pro?",
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
