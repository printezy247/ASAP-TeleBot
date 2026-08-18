import os

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
PLAN_DURATION_LABELS = {
    "en": {"1m": "1 Month", "6m": "6 Months", "1y": "1 Year"},
    "my": {"1m": "1 Bulan", "6m": "6 Bulan", "1y": "1 Tahun"},
}

# region code -> currency symbol
PRICE_REGIONS = {
    "en": "$",
    "my": "RM",
}
DEFAULT_PRICE_REGION = "en"


def plan_duration_label(duration_code: str, region: str) -> str:
    return PLAN_DURATION_LABELS.get(region, PLAN_DURATION_LABELS[DEFAULT_PRICE_REGION])[duration_code]


# code -> {name, description: {en, my}, plans: {duration_code: price}}
# Product/brand names (EzyMap, TradingView, MT5, etc.) stay in English in both
# languages. The same digits are used for both USD and the MYR promo (Malaysia/
# Indonesia/Brunei) - only the currency symbol changes based on language choice.
PRODUCTS = {
    "tv_pro": {
        "name": "TradingView - EzyMap Pro",
        "description": {
            "en": "Full EzyMap Pro indicator on TradingView with live signals M1–H4.",
            "my": "Indicator EzyMap Pro penuh di TradingView dengan live signals M1–H4.",
        },
        "plans": {"1m": "29", "6m": "149", "1y": "249"},
    },
    "mt5_bundle": {
        "name": "MT5 Indicator Bundle (Worth $999)",
        "description": {
            "en": "Complete 17 MT5 EzyMap Indicators.",
            "my": "17 Indicator EzyMap MT5 yang lengkap.",
        },
        "plans": {"1m": "99", "6m": "499", "1y": "999"},
    },
    "mt5_bulk_close": {
        "name": "Bulk Close – BONUS Layer Close (Top Selling)",
        "description": {
            "en": "Can close partial profit, number of layers with fast executions.",
            "my": "Boleh close partial profit, bilangan layer dengan eksekusi pantas.",
        },
        "plans": {"1m": "19", "6m": "109", "1y": "199"},
    },
    "mt5_drawdown_guardian": {
        "name": "Drawdown Guardian (Prop Firm Favorite)",
        "description": {
            "en": (
                "Stay alert with your current drawdown to avoid elimination from any "
                "prop firm stages."
            ),
            "my": (
                "Sentiasa alert dengan drawdown semasa anda untuk elak eliminate "
                "daripada mana-mana peringkat prop firm."
            ),
        },
        # 1m raised from $9 -> $15: below that, a card payment fails outright since
        # NOWPayments enforces a ~$12.50 minimum on USDT/TRC20 after fee deduction.
        "plans": {"1m": "15", "6m": "49", "1y": "99"},
    },
    "mt5_auto_tpsl": {
        "name": "Auto TPSL (Trending This Month)",
        "description": {
            "en": "Don't waste your time setting TP & SL manually for each layer.",
            "my": "Jimat masa anda tanpa perlu set TP & SL secara manual untuk setiap layer.",
        },
        # 1m raised from $9 -> $15: below that, a card payment fails outright since
        # NOWPayments enforces a ~$12.50 minimum on USDT/TRC20 after fee deduction.
        "plans": {"1m": "15", "6m": "49", "1y": "99"},
    },
    "mt5_currency_strength": {
        "name": "Currency Strength Meter",
        "description": {
            "en": (
                "Keep updated with the current volatility of all currencies that are "
                "mostly traded."
            ),
            "my": (
                "Sentiasa update dengan volatility semasa semua currency yang paling "
                "banyak di-trade."
            ),
        },
        # 1m raised from $9 -> $15: below that, a card payment fails outright since
        # NOWPayments enforces a ~$12.50 minimum on USDT/TRC20 after fee deduction.
        "plans": {"1m": "15", "6m": "49", "1y": "99"},
    },
    "mt5_mtf_bias": {
        "name": "MTF Bias",
        "description": {
            "en": (
                "Reveal bullish or bearish bias to give confluence for your "
                "ever-adapting trading plan."
            ),
            "my": (
                "Dedahkan bias bullish atau bearish untuk beri confluence kepada "
                "trading plan anda yang sentiasa berubah."
            ),
        },
        # 1m raised from $9 -> $15: below that, a card payment fails outright since
        # NOWPayments enforces a ~$12.50 minimum on USDT/TRC20 after fee deduction.
        "plans": {"1m": "15", "6m": "49", "1y": "99"},
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

WELCOME_MESSAGES = {
    "en": [
        (
            "Hey there my trading fam 😎\n\n"
            "I'm excited as you are, just click the button below to start and you'll "
            "get your perks right away !"
        ),
        (
            "Quick reminder before we begin ⚠️\n\n"
            "Trading involves risk. Only trade with capital you're prepared to risk, "
            "and treat any indicators as tools to support decisions, not guarantees."
        ),
        (
            f"My name's {AMBASSADOR_NAME} and I've used {BROKER_NAME} ✅ for years due "
            "to its fast withdrawals and lightning executions for faster entry and exit."
        ),
    ],
    "my": [
        (
            "Hai semua income hustler 💪\n\n"
            "Jack pun excited macam korang, klik je button bawah tu untuk mula dan "
            "akan terus produk yang korang nak!"
        ),
        (
            "Peringatan sebelum kita mula ⚠️\n\n"
            "Trading melibatkan risiko. Hanya trade dengan modal yang sanggup "
            "risikokan, dan anggap indicator untuk support analysis, bukan confirm "
            "jadi."
        ),
        (
            f"Saya {AMBASSADOR_NAME} and {BROKER_NAME} memang favorite sebab "
            "withdraw laju and fast execution untuk entry exit sepantas kilat."
        ),
        "Pilih satu option dekat bawah 👇",
    ],
}

LANGUAGE_SELECT_TEXT = "🌐 Choose your language / Pilih bahasa anda:"

MAIN_MENU_TEXT = {
    "en": "What would you like to do?",
    "my": "Apa yang anda ingin buat?",
}

BROKER_INFO_TEXT = {
    "en": (
        f"📘 *Why Choose {BROKER_NAME}*\n\n"
        f"We partner with {BROKER_NAME} for trading. You can check them out directly "
        f"here:\n{BROKER_WEBSITE}"
    ),
    "my": (
        f"📘 *Kenapa Pilih {BROKER_NAME}*\n\n"
        f"Kami bekerjasama dengan {BROKER_NAME} untuk trading. Anda boleh semak terus "
        f"di sini:\n{BROKER_WEBSITE}"
    ),
}

PACKAGES_INTRO_TEXT = {
    "en": (
        f"🎁 *{CHANNEL_NAME} FREE Steps*\n\n"
        f"Everything is unlocked by having a trading account under my IB (`{IB_NUMBER}`) "
        f"with {BROKER_NAME}. The more you have with them, the more you unlock. No "
        f"extra payment needed for these.\n\n"
        "Pick a package to see what it includes:"
    ),
    "my": (
        f"🎁 *Langkah PERCUMA {CHANNEL_NAME}*\n\n"
        f"Semuanya dibuka hanya dengan membuka akaun trading di bawah IB saya "
        f"(`{IB_NUMBER}`) bersama {BROKER_NAME}. Semakin banyak anda ada dengan "
        f"mereka, semakin banyak yang anda buka. Tiada bayaran tambahan diperlukan "
        f"untuk semua ini.\n\n"
        "Pilih pakej untuk lihat apa yang disertakan:"
    ),
}

# key -> {"name": tier display name (unchanged across languages), "detail": {en, my}}
# Keys match the "tier_<key>" callback_data used in keyboards.package_tier_menu(), and
# are stored in context.user_data so the admin notification can show which package
# the client picked.
PACKAGE_TIERS = {
    "beginner": {
        "name": "Beginner",
        "detail": {
            "en": (
                "🥉 *Beginner Package*\n\n"
                f"Requirement: open an account under my IB (`{IB_NUMBER}`), no "
                f"deposit needed.\n\n"
                "You will get:\n"
                "• eBook: Technical Analysis & Mapping Like A Pro\n"
                "• Indicator EzyMap Lite (TradingView)"
            ),
            "my": (
                "🥉 *Pakej Beginner*\n\n"
                f"Keperluan: buka akaun di bawah IB saya (`{IB_NUMBER}`), tiada "
                f"deposit diperlukan.\n\n"
                "Anda akan dapat:\n"
                "• eBook: Technical Analysis & Mapping Like A Pro\n"
                "• Indicator EzyMap Lite (TradingView)"
            ),
        },
    },
    "pro": {
        "name": "Pro",
        "detail": {
            "en": (
                "🥈 *Pro Package*\n\n"
                f"Requirement: open an account under my IB (`{IB_NUMBER}`) + deposit "
                f"(any amount).\n\n"
                "You will get:\n"
                "• EzyScalper = M1 & M5 private signal channel\n"
                "• EzyMap MT5 Indicator = Currency Strength Meter\n"
                "• Everything in the Beginner"
            ),
            "my": (
                "🥈 *Pakej Pro*\n\n"
                f"Keperluan: buka akaun di bawah IB saya (`{IB_NUMBER}`) + deposit "
                f"(apa-apa jumlah).\n\n"
                "Anda akan dapat:\n"
                "• EzyScalper = M1 & M5 private signal channel\n"
                "• EzyMap MT5 Indicator = Currency Strength Meter\n"
                "• Semua dalam pakej Beginner"
            ),
        },
    },
    "premium": {
        "name": "Premium",
        "detail": {
            "en": (
                "🥇 *Premium Package*\n\n"
                f"Requirement: open an account under my IB (`{IB_NUMBER}`) + deposit "
                f"min $100.\n\n"
                "You will get:\n"
                "• EzyMap Pro Indicator (TradingView) = M1–H4 signals\n"
                "• EzyMap MT5 Indicator = Auto TPSL & MTF Bias\n"
                "• EzyIntraday = M15 & M30 private signal channel\n"
                "• Everything in the Pro"
            ),
            "my": (
                "🥇 *Pakej Premium*\n\n"
                f"Keperluan: buka akaun di bawah IB saya (`{IB_NUMBER}`) + deposit "
                f"minimum $100.\n\n"
                "Anda akan dapat:\n"
                "• EzyMap Pro Indicator (TradingView) = M1–H4 signals\n"
                "• EzyMap MT5 Indicator = Auto TPSL & MTF Bias\n"
                "• EzyIntraday = M15 & M30 private signal channel\n"
                "• Semua dalam pakej Pro"
            ),
        },
    },
    "elite": {
        "name": "Elite",
        "detail": {
            "en": (
                "🏆 *Elite Package*\n\n"
                f"Requirement: open an account under my IB (`{IB_NUMBER}`) + deposit "
                f"min $700.\n\n"
                "You will get:\n"
                "• EzyMap MT5 Indicator = Drawdown Guardian, Bulk Close with Layer "
                "Close Function, Auto TPSL, and 5 more (worth $249)\n"
                "• EzySwing = H1 & H4 private signal channel\n"
                "• Ezy Elite Circle = 1-on-1 support from Jack\n"
                "• Everything in the Premium"
            ),
            "my": (
                "🏆 *Pakej Elite*\n\n"
                f"Keperluan: buka akaun di bawah IB saya (`{IB_NUMBER}`) + deposit "
                f"minimum $700.\n\n"
                "Anda akan dapat:\n"
                "• EzyMap MT5 Indicator = Drawdown Guardian, Bulk Close with Layer "
                "Close Function, Auto TPSL, dan 5 lagi (bernilai $249)\n"
                "• EzySwing = H1 & H4 private signal channel\n"
                "• Ezy Elite Circle = sokongan 1-on-1 daripada Jack\n"
                "• Semua dalam pakej Premium"
            ),
        },
    },
}

# tier key -> promotional image shown above the tier detail text. Value can be a public
# URL (Telegram fetches it directly, no upload needed) or a path to a local file in this
# repo (opened and uploaded). Leave blank to keep showing plain text for that tier.
_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_TIER_IMAGES = {
    "beginner": os.path.join(_MODULE_DIR, "1.beginner.png"),
    "pro": os.path.join(_MODULE_DIR, "2.pro.png"),
    "premium": os.path.join(_MODULE_DIR, "3.premium.png"),
    "elite": os.path.join(_MODULE_DIR, "4.elite.png"),
}

OPEN_ACCOUNT_TEXT = {
    "en": (
        "💠 *Open a New Account*\n\n"
        f"1️⃣ Click this link to open your account under my IB: {OPEN_ACCOUNT_LINK}\n"
        "2️⃣ Complete the sign-up form with your real details.\n"
        "3️⃣ Verify your email and identity as prompted by "
        f"{BROKER_NAME}. Be honest, you'll need this to withdraw later.\n\n"
        "Once your account is open (and deposited, if you're going for Pro/Premium), "
        "tap *✅ I've Completed Registration* below to send me your details."
    ),
    "my": (
        "💠 *Buka Akaun Baharu*\n\n"
        f"1️⃣ Klik link ini untuk buka akaun anda di bawah IB saya: {OPEN_ACCOUNT_LINK}\n"
        "2️⃣ Lengkapkan borang pendaftaran dengan maklumat sebenar anda.\n"
        "3️⃣ Sahkan email dan identiti anda seperti diminta oleh "
        f"{BROKER_NAME}. Jujurlah, anda perlukan ini untuk buat pengeluaran nanti.\n\n"
        "Setelah akaun anda dibuka (dan deposit, jika anda pilih Pro/Premium), tekan "
        "*✅ Saya Telah Selesai Daftar* di bawah untuk hantar maklumat anda."
    ),
}

CHANGE_IB_TEXT = {
    "en": (
        "🔁 *Change IB* (only for those who already have a Vantage Markets account)\n\n"
        "This one's done by email, not a link. Send an email with these exact details:\n\n"
        f"To: `{CHANGE_IB_EMAIL_TO}`\n"
        f"Cc: `{CHANGE_IB_EMAIL_CC}`\n"
        "Subject: `Account reassign`\n\n"
        "Body:\n"
        "```\n"
        "Hi,\n\n"
        f"Kindly assist to reassign my account under ({IB_NUMBER}) as he is helping me "
        "on my account.\n\n"
        "Email client: *your registered email* ✅\n\n"
        "Thank you\n"
        "```\n\n"
        "Replace *your registered email* with the email your Vantage account is "
        "registered under, then send it. Once done, tap "
        "*✅ I've Completed Registration* below."
    ),
    "my": (
        "🔁 *Tukar IB* (hanya untuk yang sudah ada akaun Vantage Markets)\n\n"
        "Ini dibuat melalui email, bukan link. Hantar email dengan maklumat ini dengan "
        "tepat:\n\n"
        f"Kepada: `{CHANGE_IB_EMAIL_TO}`\n"
        f"Cc: `{CHANGE_IB_EMAIL_CC}`\n"
        "Subjek: `Account reassign`\n\n"
        "Kandungan:\n"
        "```\n"
        "Hi,\n\n"
        f"Kindly assist to reassign my account under ({IB_NUMBER}) as he is helping me "
        "on my account.\n\n"
        "Email client: *email berdaftar anda* ✅\n\n"
        "Thank you\n"
        "```\n\n"
        "Gantikan *email berdaftar anda* dengan email yang akaun Vantage anda "
        "daftarkan, kemudian hantar. Setelah selesai, tekan "
        "*✅ Saya Telah Selesai Daftar* di bawah."
    ),
}

SUBMIT_DETAILS_PROMPT = {
    "en": (
        "✅ Great! Let's get your details sent over so Jack can check your account "
        "and unlock your package.\n\n"
        "What's your *full name*?"
    ),
    "my": (
        "✅ Bagus! Mari hantar maklumat anda supaya Jack boleh semak akaun anda dan "
        "buka pakej anda.\n\n"
        "Apakah *nama penuh* anda?"
    ),
}
ASK_EMAIL_TEXT = {
    "en": "Got it. What's the *email* you registered with?",
    "my": "Baik. Apakah *email* yang anda gunakan untuk daftar?",
}
ASK_ACCOUNT_TEXT = {
    "en": "Thanks. What's your *account number*?",
    "my": "Terima kasih. Apakah *nombor akaun* anda?",
}
ASK_DEPOSIT_PROOF_TEXT = {
    "en": (
        "Almost done! Since this package requires a deposit, please send a "
        "*screenshot of your deposit proof*."
    ),
    "my": (
        "Hampir siap! Oleh kerana pakej ini memerlukan deposit, sila hantar "
        "*screenshot bukti deposit* anda."
    ),
}

SUBMISSION_CONFIRMATION_TEXT = {
    "en": (
        "🎉 Thanks! Your details have been sent to Jack for review.\n\n"
        "Your package perks will be unlocked shortly based on your account status. If "
        "you have questions in the meantime, check the FAQ from the main menu."
    ),
    "my": (
        "🎉 Terima kasih! Maklumat anda telah dihantar kepada Jack untuk semakan.\n\n"
        "Perks pakej anda akan dibuka tidak lama lagi berdasarkan status akaun anda. "
        "Jika ada soalan, semak FAQ di menu utama."
    ),
}
SUBMISSION_ADMIN_UNREACHABLE_TEXT = {
    "en": (
        "🎉 Thanks, I've got your details!\n\n"
        "I couldn't reach Jack automatically just now, but your submission was "
        "recorded. Please also message the admin directly to be safe. Your perks "
        "will be unlocked shortly."
    ),
    "my": (
        "🎉 Terima kasih, maklumat anda telah diterima!\n\n"
        "Saya tidak dapat hubungi Jack secara automatik buat masa ini, tetapi "
        "maklumat anda telah direkodkan. Sila mesej admin terus untuk memastikan. "
        "Perks anda akan dibuka tidak lama lagi."
    ),
}

# Sent to the client the moment Jack taps Approve/Reject on their registration
# notification. {label} is the package tier name (e.g. "Pro").
REGISTRATION_APPROVED_TEXT = {
    "en": "🎉 Great news! Your {label} package has been approved and unlocked. Thanks for your patience!",
    "my": "🎉 Berita baik! Pakej {label} anda telah diluluskan dan dibuka. Terima kasih atas kesabaran anda!",
}
REGISTRATION_REJECTED_TEXT = {
    "en": (
        "Hey, I wasn't able to verify your registration this time. Please double check "
        "your details or message the admin directly."
    ),
    "my": (
        "Hai, saya tak dapat sahkan pendaftaran anda kali ini. Sila semak semula "
        "maklumat anda atau mesej admin terus."
    ),
}

CANCEL_TEXT = {
    "en": "Cancelled. Use /start any time to open the menu again.",
    "my": "Dibatalkan. Guna /start bila-bila masa untuk buka menu semula.",
}

PURCHASE_INTRO_TEXT = {
    "en": (
        "💎 *Purchase EzyMap*\n\n"
        "These are paid, separate from your broker account. Pick a category:"
    ),
    "my": (
        "💎 *Beli EzyMap*\n\n"
        "Ini adalah item berbayar, berasingan daripada akaun broker anda. Pilih "
        "kategori:"
    ),
}

FAQ_LIST_HEADER = {
    "en": "❓ *FAQ*: tap a question to see the answer.",
    "my": "❓ *Soalan Lazim*: tekan soalan untuk lihat jawapan.",
}

MT5_BUNDLES_INTRO_TEXT = {
    "en": (
        "🖥 *MT5 - EzyMap Bundles*\n\n"
        "Pick an indicator (or the full bundle) to see pricing:"
    ),
    "my": (
        "🖥 *MT5 - EzyMap Bundles*\n\n"
        "Pilih satu indicator (atau bundle penuh) untuk lihat harga:"
    ),
}


def product_detail_text(product_code: str, region: str) -> str:
    product = PRODUCTS[product_code]
    description = product["description"].get(region, product["description"][DEFAULT_PRICE_REGION])
    pick_plan = "Pilih pelan:" if region == "my" else "Pick a plan:"
    lines = [f"💎 *{product['name']}*", "", description, "", pick_plan]
    return "\n".join(lines)


def plan_button_label(product_code: str, duration_code: str, region: str = DEFAULT_PRICE_REGION) -> str:
    price = PRODUCTS[product_code]["plans"][duration_code]
    duration_label = plan_duration_label(duration_code, region)
    symbol = PRICE_REGIONS.get(region, PRICE_REGIONS[DEFAULT_PRICE_REGION])
    return f"{duration_label} ({symbol}{price})"


CHOOSE_PAYMENT_METHOD_TEXT = {
    "en": "💎 *{product_name} ({plan_name})*\nPrice: *{price}*\n\nHow would you like to pay?",
    "my": "💎 *{product_name} ({plan_name})*\nHarga: *{price}*\n\nBagaimana anda ingin bayar?",
}

# USDT is always quoted in USD, regardless of the client's chosen pricing region, since
# crypto amounts are inherently dollar-denominated.
PAYMENT_PROMPT_TEMPLATE = {
    "en": (
        "💎 *{product_name} ({plan_name})*\n"
        "Price: *${price} USD*\n\n"
        "Send exactly *{price} USDT* ({network} network) to:\n"
        f"`{USDT_WALLET_ADDRESS}`\n\n"
        "⚠️ Send USDT only, on the *{network}* network. Wrong coin or wrong network "
        "can lose your funds.\n\n"
        "Once sent, reply here with a *screenshot of the transfer* or your "
        "*transaction ID*, and Jack will confirm and activate your purchase.\n\n"
        "Prefer a different way to pay? Tap the button below to message Jack directly."
    ),
    "my": (
        "💎 *{product_name} ({plan_name})*\n"
        "Harga: *${price} USD*\n\n"
        "Hantar tepat *{price} USDT* (rangkaian {network}) ke:\n"
        f"`{USDT_WALLET_ADDRESS}`\n\n"
        "⚠️ Hantar USDT sahaja, pada rangkaian *{network}*. Coin atau rangkaian yang "
        "salah boleh menyebabkan dana anda hilang.\n\n"
        "Setelah dihantar, balas di sini dengan *screenshot pemindahan* atau "
        "*transaction ID* anda, dan Jack akan sahkan dan aktifkan pembelian anda.\n\n"
        "Mahu cara bayaran lain? Tekan butang di bawah untuk mesej Jack terus."
    ),
}


CARD_UNAVAILABLE_TEXT = {
    "en": "Card payment isn't available right now. Please use USDT instead, or message Jack directly.",
    "my": "Pembayaran kad tidak tersedia buat masa ini. Sila guna USDT, atau mesej Jack terus.",
}
CARD_INVOICE_CREATED_TEXT = {
    "en": (
        "💎 *{product_name} ({plan_name})*\n"
        "Price: *${price} USD*\n\n"
        "Tap below to pay securely by card or e-wallet. Once payment goes through, "
        "your purchase is confirmed automatically - no need to send proof."
    ),
    "my": (
        "💎 *{product_name} ({plan_name})*\n"
        "Harga: *${price} USD*\n\n"
        "Tekan di bawah untuk bayar dengan selamat menggunakan kad atau e-wallet. "
        "Setelah pembayaran berjaya, pembelian anda disahkan secara automatik - tiada "
        "keperluan hantar bukti."
    ),
}
CARD_INVOICE_FAILED_TEXT = {
    "en": "Sorry, I couldn't start a card payment right now. Please use USDT instead, or message Jack directly.",
    "my": "Maaf, saya tidak dapat mulakan pembayaran kad buat masa ini. Sila guna USDT, atau mesej Jack terus.",
}

PAYMENT_PROOF_RECEIVED_TEXT = {
    "en": (
        "✅ Got it! Your payment proof has been sent to Jack.\n\n"
        "He'll confirm and activate your purchase shortly. If you have questions in "
        "the meantime, check the FAQ from the main menu."
    ),
    "my": (
        "✅ Diterima! Bukti pembayaran anda telah dihantar kepada Jack.\n\n"
        "Dia akan sahkan dan aktifkan pembelian anda tidak lama lagi. Jika ada "
        "soalan, semak FAQ di menu utama."
    ),
}
PAYMENT_PROOF_ADMIN_UNREACHABLE_TEXT = {
    "en": (
        "✅ Got your payment proof!\n\n"
        "I couldn't reach Jack automatically just now. Please also message the "
        "admin directly with your proof to be safe. Your purchase will be activated "
        "shortly after."
    ),
    "my": (
        "✅ Bukti pembayaran diterima!\n\n"
        "Saya tidak dapat hubungi Jack secara automatik buat masa ini. Sila mesej "
        "admin terus dengan bukti anda untuk memastikan. Pembelian anda akan "
        "diaktifkan tidak lama lagi selepas itu."
    ),
}

# Sent to the client the moment Jack taps Approve/Reject on their payment proof
# notification. {label} is "{product_name} ({plan_name})".
PAYMENT_APPROVED_TEXT = {
    "en": "🎉 Payment confirmed! Your {label} purchase is now active. Enjoy!",
    "my": "🎉 Pembayaran disahkan! Pembelian {label} anda kini aktif. Nikmati!",
}
PAYMENT_REJECTED_TEXT = {
    "en": (
        "Hey, I wasn't able to verify your payment this time. Please double check or "
        "message the admin directly."
    ),
    "my": (
        "Hai, saya tak dapat sahkan pembayaran anda kali ini. Sila semak semula atau "
        "mesej admin terus."
    ),
}

TRADINGVIEW_FREE_URL = (
    "https://www.tradingview.com/pricing/?share_your_love=printezyusd&mobileapp=true"
)

# Each item: {"question": {en,my}, "answer": {en,my}, "show_contact_admin": bool,
#             "extra_button": None or {"label": {en,my}, "url": str}}
FAQ_ITEMS = [
    {
        "question": {
            "en": "Is joining EzyMap Algo free?",
            "my": "Adakah menyertai EzyMap Algo percuma?",
        },
        "answer": {
            "en": (
                "Yes, Beginner, Pro, Premium, and Elite are all unlocked just by "
                f"having an account under my IB with {BROKER_NAME} (Premium and Elite "
                "also need a minimum deposit). Only the *Purchase EzyMap* items "
                "(TradingView Pro or the MT5 bundles) cost money."
            ),
            "my": (
                "Ya, Beginner, Pro, Premium, dan Elite semuanya dibuka hanya dengan "
                f"membuka akaun di bawah IB saya bersama {BROKER_NAME} (Premium dan "
                "Elite juga perlukan deposit minimum). Hanya item *Beli EzyMap* "
                "(TradingView Pro atau MT5 bundles) yang berbayar."
            ),
        },
        "show_contact_admin": False,
        "extra_button": None,
    },
    {
        "question": {
            "en": "What's the difference between the free packages and Purchase EzyMap?",
            "my": "Apakah perbezaan antara pakej percuma dan Beli EzyMap?",
        },
        "answer": {
            "en": (
                "The free packages (Beginner/Pro/Premium/Elite) are unlocked by your "
                "broker account status under my IB. *Purchase EzyMap* is separate "
                "paid content: the TradingView EzyMap Pro indicator, or the MT5 "
                "indicator bundle/individual tools."
            ),
            "my": (
                "Pakej percuma (Beginner/Pro/Premium/Elite) dibuka berdasarkan status "
                "akaun broker anda di bawah IB saya. *Beli EzyMap* adalah kandungan "
                "berbayar berasingan: indicator EzyMap Pro TradingView, atau MT5 "
                "indicator bundle/individu."
            ),
        },
        "show_contact_admin": False,
        "extra_button": None,
    },
    {
        "question": {
            "en": "How much do I need to deposit?",
            "my": "Berapa banyak deposit yang saya perlukan?",
        },
        "answer": {
            "en": (
                "Beginner needs no deposit. Pro needs any deposit amount. Premium "
                "needs a minimum $100 deposit. Elite needs a minimum $700 deposit. "
                "All under my IB."
            ),
            "my": (
                "Beginner tak perlu deposit. Pro perlukan sebarang jumlah deposit. "
                "Premium perlukan deposit minimum $100. Elite perlukan deposit "
                "minimum $700. Semua di bawah IB saya."
            ),
        },
        "show_contact_admin": False,
        "extra_button": None,
    },
    {
        "question": {
            "en": "What do I get with the Elite package?",
            "my": "Apa yang saya dapat dengan pakej Elite?",
        },
        "answer": {
            "en": (
                "Everything in Premium, plus the full EzyMap MT5 indicator set "
                "(Drawdown Guardian, Bulk Close with Layer Close, Auto TPSL, and more, "
                "worth $249), and the Ezy Elite Circle with 1-on-1 support from Jack."
            ),
            "my": (
                "Semua dalam Premium, ditambah set penuh indicator EzyMap MT5 "
                "(Drawdown Guardian, Bulk Close with Layer Close, Auto TPSL, dan "
                "banyak lagi, bernilai $249), serta Ezy Elite Circle dengan sokongan "
                "1-on-1 daripada Jack."
            ),
        },
        "show_contact_admin": False,
        "extra_button": None,
    },
    {
        "question": {
            "en": "I already have a Vantage account. Can I still join?",
            "my": "Saya sudah ada akaun Vantage. Boleh saya sertai juga?",
        },
        "answer": {
            "en": (
                "Yes, use *Change IB* instead of opening a new account (it's done by "
                "email, not a link), then submit your details the same way."
            ),
            "my": (
                "Boleh, guna *Tukar IB* dan bukannya buka akaun baharu (dibuat "
                "melalui email, bukan link), kemudian hantar maklumat anda dengan "
                "cara yang sama."
            ),
        },
        "show_contact_admin": False,
        "extra_button": None,
    },
    {
        "question": {
            "en": "How long until my package is unlocked?",
            "my": "Berapa lama sebelum pakej saya dibuka?",
        },
        "answer": {
            "en": (
                "Once you submit your Name, Email, and Account Number, Jack checks "
                "your account status and unlocks the matching package shortly after, "
                "usually the same day."
            ),
            "my": (
                "Setelah anda hantar Nama, Email, dan Nombor Akaun, Jack akan semak "
                "status akaun anda dan buka pakej yang sesuai, biasanya pada hari "
                "yang sama."
            ),
        },
        "show_contact_admin": False,
        "extra_button": None,
    },
    {
        "question": {
            "en": "How do I pay for a paid indicator or bundle?",
            "my": "Bagaimana saya bayar untuk indicator atau bundle berbayar?",
        },
        "answer": {
            "en": (
                "Tap *💎 Purchase EzyMap* from the main menu, pick TradingView or "
                "MT5, then a plan. You'll be asked to pay via USDT (wallet address + "
                "confirm with Jack) or via Card/Bank/E-Wallet, which confirms "
                "automatically once payment goes through."
            ),
            "my": (
                "Tekan *💎 Beli EzyMap* di menu utama, pilih TradingView atau MT5, "
                "kemudian pilih pelan. Anda akan diminta bayar melalui USDT (alamat "
                "wallet + sahkan dengan Jack) atau Card/Bank/E-Wallet, yang akan "
                "disahkan secara automatik sebaik sahaja pembayaran berjaya."
            ),
        },
        "show_contact_admin": False,
        "extra_button": None,
    },
    {
        "question": {
            "en": "Can I cancel or get a refund on a paid indicator/bundle?",
            "my": "Bolehkah saya batalkan atau dapatkan refund untuk indicator/bundle berbayar?",
        },
        "answer": {
            "en": (
                "Message Jack directly to discuss. Refund/cancellation isn't "
                "handled automatically through the bot."
            ),
            "my": (
                "Mesej Jack terus untuk berbincang. Pembatalan/refund tidak "
                "dikendalikan secara automatik melalui bot."
            ),
        },
        "show_contact_admin": True,
        "extra_button": None,
    },
    {
        "question": {
            "en": "Do I need TradingView for the indicators?",
            "my": "Perlukah saya guna TradingView untuk indicator-indicator ini?",
        },
        "answer": {
            "en": (
                "The TradingView EzyMap indicators (Lite/Scalp Mastery/Pro) need a "
                "free or paid TradingView account. The MT5 bundle and individual "
                "tools (Drawdown Guardian, Bulk Close, Auto TPSL, Currency Strength "
                "Meter, MTF Bias) run on MT5 instead. No TradingView needed for those."
            ),
            "my": (
                "Indicator EzyMap TradingView (Lite/Scalp Mastery/Pro) memerlukan "
                "akaun TradingView percuma atau berbayar. Bundle MT5 dan alat "
                "individu (Drawdown Guardian, Bulk Close, Auto TPSL, Currency "
                "Strength Meter, MTF Bias) berjalan di MT5. Tak perlukan TradingView "
                "untuk yang ini."
            ),
        },
        "show_contact_admin": False,
        "extra_button": {
            "label": {"en": "📊 Get TradingView FREE", "my": "📊 Dapatkan TradingView PERCUMA"},
            "url": TRADINGVIEW_FREE_URL,
        },
    },
    {
        "question": {
            "en": "What if I get stuck during registration or payment?",
            "my": "Apa perlu saya buat jika saya stuck semasa pendaftaran atau pembayaran?",
        },
        "answer": {
            "en": (
                "Go through the Open Account or Change IB steps again from the menu, "
                "or tap the button below to message Jack directly."
            ),
            "my": (
                "Ulang langkah Open Account atau Change IB dari menu, atau tekan "
                "butang di bawah untuk mesej Jack terus."
            ),
        },
        "show_contact_admin": True,
        "extra_button": None,
    },
]
