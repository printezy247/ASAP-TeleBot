CHANNEL_NAME = "A$AP USD"
AMBASSADOR_NAME = "Asad"
BROKER_NAME = "Elev8"
IB_NUMBER = "20165521"
OPEN_ACCOUNT_LINK = "https://clickto.trade/bT1xuKbNO1t?ib=20165521"
CHANGE_IB_LINK = "https://clickto.trade/bXV6kLY1rKv?ib=20165521"
BROKER_WEBSITE = "https://en.elev8trade.net/"

WELCOME_MESSAGES = [
    (
        f"👋 Welcome to *{CHANNEL_NAME}*!\n\n"
        f"I'm your registration assistant, here to get you set up fast — no waiting on a human "
        f"to answer the same questions over and over. Let's get you started."
    ),
    (
        "⚠️ *Quick risk reminder before we begin*\n\n"
        "Trading involves risk, and you should only trade with capital you're prepared to risk. "
        "How much capital are you comfortable risking on your trades? Keep this in mind as we go "
        "through registration — it's on you to trade responsibly."
    ),
    (
        f"✅ Alright, let's go! Everything below is done with buttons — just tap your way through.\n\n"
        f"Ambassador: *{AMBASSADOR_NAME}* | Broker: *{BROKER_NAME}*"
    ),
]

MAIN_MENU_TEXT = "What would you like to do?"

BROKER_INFO_TEXT = (
    f"📘 *About {BROKER_NAME}*\n\n"
    f"We partner with {BROKER_NAME} for trading. You can check them out directly here:\n"
    f"{BROKER_WEBSITE}"
)

SIGNALS_INTRO_TEXT = (
    "🚦 *Get My Free Signals*\n\n"
    f"To get access to the VIP signals channel, you need to have a trading account open under "
    f"my IB (`{IB_NUMBER}`) with {BROKER_NAME}. *No deposit is required* — just a registered "
    f"account under my IB.\n\n"
    "Pick what applies to you:"
)

OPEN_ACCOUNT_TEXT = (
    "💠 *Registration & Verification*\n\n"
    f"1️⃣ Click the link below to create your free trading account:\n{OPEN_ACCOUNT_LINK}\n\n"
    "2️⃣ Fill out the form or sign up with Facebook, Google, or Apple ID.\n"
    "   • Enter your real email — you'll confirm it.\n"
    "   • Set a password — used for all trading accounts.\n"
    "   • Press *Sign Up* to proceed.\n\n"
    "3️⃣ Check your email. In the letter from us, press *Confirm*.\n\n"
    "4️⃣ Provide your personal details and press *Continue*. Be honest — you'll need to verify "
    "your identity later to withdraw money.\n\n"
    "5️⃣ Configure your new account:\n"
    "   🌟 Standard account\n"
    "   🌟 MT4/MT5\n"
    "   🌟 Real\n"
    "   🌟 USD (or your preferred currency)\n"
    "   🌟 Leverage 1:500\n"
    "   🌟 Swap: off (fixed rate)\n\n"
    f"6️⃣ Press *Create Account* to finish registration.\n\n"
    f"7️⃣ Verify your account with {BROKER_NAME}:\n"
    "   ✅ You need your NRIC (National Registration Identity Card)\n"
    "   ✅ Upload the full-size coloured image\n"
    "   ✅ Do not upload selfies, screenshots, or edited images\n\n"
    "Once done, tap *✅ I've Completed Registration* below to send me your details."
)

CHANGE_IB_TEXT = (
    "🔁 *Change IB* (only for those who already have an Elev8 account)\n\n"
    f"1️⃣ Click this link: {CHANGE_IB_LINK}\n"
    f"2️⃣ Fill in IB number: `{IB_NUMBER}`\n"
    '3️⃣ Fill in the reason: "Easy for me to get guidance and help in trading."\n'
    "4️⃣ Click *Send request*\n\n"
    "Once done, tap *✅ I've Completed Registration* below to send me your details."
)

DEPOSIT_INTRO_TEXT = (
    "💰 *Deposit*\n\n"
    "1️⃣ Log in to your profile.\n"
    "2️⃣ Press *New Deposit*.\n"
    "3️⃣ Select the account you want to top up.\n"
    "4️⃣ Choose your preferred transfer method.\n\n"
    "The available payment methods depend on the country you registered with. "
    "Pick a method below for a step-by-step guide:"
)

DEPOSIT_BANK_TEXT = (
    "🏦 *Deposit via Local Bank*\n\n"
    "1️⃣ Select the *Local Bank* option or choose your bank from the list. If you don't see this "
    "option, it may only be available to verified users — verify your account and try again.\n"
    "2️⃣ Specify the deposit amount.\n"
    "3️⃣ Adjust your bonus percentage (select your bank first if you haven't).\n"
    "4️⃣ Choose how to transfer: online banking app, ATM, or a bank branch.\n"
    "5️⃣ Make the transfer using the bank details shown on the deposit page. Keep the payment "
    "document.\n"
    "6️⃣ The amount you specify on the site must match what you actually transfer, or processing "
    "will be delayed. You can only deposit from your own bank account.\n"
    "7️⃣ When done, press *Notify Us After Transfer* and fill in the amount, your bank account "
    "number, and the payment date.\n"
    "8️⃣ Upload the payment document via *Continue* to speed things up, then wait for "
    "confirmation.\n\n"
    "⏱ Usually takes 1–3 hours."
)

DEPOSIT_CARD_TEXT = (
    "💳 *Deposit via Card / E-Wallet*\n\n"
    "1️⃣ Select Visa, Mastercard, or your preferred e-wallet (availability varies by region).\n"
    "2️⃣ Enter the amount or choose a suggested option.\n"
    "3️⃣ Adjust your bonus percentage and fill in any additional payment info. Check the transfer "
    "details.\n"
    "4️⃣ Follow the instructions on the payment service page to complete the payment.\n\n"
    "⏱ Usually near-instant, sometimes up to 30 minutes."
)

DEPOSIT_BTC_TEXT = (
    "₿ *Deposit via Bitcoin (BTC)*\n\n"
    "1️⃣ Select the Bitcoin option.\n"
    "2️⃣ Adjust your bonus percentage.\n"
    "3️⃣ Make sure you're within the daily deposit limit of 20,000 USD, then press *Proceed with "
    "BTC*.\n"
    "4️⃣ Use your crypto wallet — scan the QR code or copy the Bitcoin address and make the "
    "payment.\n\n"
    "⏱ Usually a few minutes, sometimes up to 30 minutes."
)

DEPOSIT_USDT_TEXT = (
    "🟢 *Deposit via Tether (USDT)*\n\n"
    "1️⃣ Select ERC20 or TRC20 — make sure you transfer on the *same network*, or your funds "
    "will be lost.\n"
    "2️⃣ Adjust your bonus percentage.\n"
    "3️⃣ Make sure you're above the minimum deposit of 50 ₮, then press *Proceed with Tether*.\n"
    "4️⃣ Use your crypto wallet — scan the QR code or copy the address and make the payment.\n\n"
    "⏱ Usually a few minutes, sometimes up to 30 minutes."
)

WITHDRAW_TEXT = (
    "💸 *Withdraw*\n\n"
    "⚠️ You can only withdraw after verifying your profile — this is required by law.\n\n"
    "1️⃣ Log in to your Personal Area.\n"
    "   • From your *Wallet*: open the ≡ menu at the top-right.\n"
    "   • From a *trading account*: select the account on the main screen, then press "
    "*Withdraw*.\n"
    "2️⃣ Pick a payment option available in your region and press *Next*.\n\n"
    "⏱ Requests are usually processed in 1–3 hours; total time also depends on your payment "
    "system.\n\n"
    "*Limits:*\n"
    "• Skrill, Perfect Money, Neteller — from 5 USD, no max\n"
    "• Bitcoin — from 0.00096 BTC, no max\n"
    "• Visa — from 20 USD (or currency equivalent)\n"
    "• Banks may apply their own limits\n\n"
    "3️⃣ Enter the details for your selected method and press *Request* — make sure the currency "
    "is correct.\n"
    "4️⃣ Double-check everything and confirm by pressing *Submit* again.\n\n"
    "You'll get a notice once the money is sent, by email and in your Personal Area."
)

SUBMIT_DETAILS_PROMPT = (
    "✅ Great — let's get your details sent over so you can be added to the VIP channel.\n\n"
    "What's your *full name*?"
)

ASK_EMAIL_TEXT = "Got it. What's the *email* you registered with?"
ASK_ACCOUNT_TEXT = "Thanks. What's your *account number*?"

SUBMISSION_CONFIRMATION_TEXT = (
    "🎉 Thanks! Your details have been sent to the admin for review.\n\n"
    "You'll be added to the VIP signals channel shortly. If you have questions in the meantime, "
    "check the FAQ from the main menu."
)

SUBMISSION_ADMIN_UNREACHABLE_TEXT = (
    "🎉 Thanks, I've got your details!\n\n"
    "I couldn't reach the admin automatically just now, but your submission was recorded — "
    "please also send your Name, Email, and Account Number directly to the admin to be safe. "
    "You'll be added to the VIP signals channel shortly."
)

CANCEL_TEXT = "Cancelled. Use /start any time to open the menu again."

FAQ_ITEMS = [
    (
        "Is this really free?",
        "Yes. There's no cost to join the VIP signals channel — you just need a trading account "
        f"opened under my IB with {BROKER_NAME}. No deposit required.",
        False,
    ),
    (
        "Do I need to deposit money?",
        "No deposit is required to get access to the free signals channel. You only need to "
        "open an account (or switch your IB) under my link.",
        False,
    ),
    (
        "How long until I get VIP access?",
        "Once you submit your Name, Email, and Account Number, the admin reviews it and adds "
        "you shortly after — usually the same day.",
        False,
    ),
    (
        "I already have an Elev8 account. Can I still join?",
        "Yes — use the *Change IB* option instead of opening a new account, then submit your "
        "details the same way.",
        False,
    ),
    (
        "Is it safe / is this broker regulated?",
        f"We work with {BROKER_NAME}. You can review their site and terms directly at "
        f"{BROKER_WEBSITE} before signing up.",
        False,
    ),
    (
        "What if I get stuck during registration?",
        "Go through the Open Account or Change IB steps again from the menu, or tap the button "
        "below to message the admin directly.",
        True,
    ),
]
