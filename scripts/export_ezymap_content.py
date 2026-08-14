"""One-off script: dumps every EzyMap Algo bot message and button label (English +
Bahasa Melayu) into a readable reference .txt file. Not used by the bot itself -
just a way to keep content.py as the single source of truth while still giving a
plain-text copy for reference/editing outside the code.

Usage: python scripts/export_ezymap_content.py [output_path]
"""

import sys

from ezymap_bot import content, keyboards


def line(out, text=""):
    out.append(text)


def section(out, title):
    line(out)
    line(out, "=" * 70)
    line(out, title)
    line(out, "=" * 70)


def bilingual(out, label, text_dict):
    line(out, f"[{label}]")
    line(out, f"  EN: {text_dict.get('en', '')}")
    line(out, f"  MY: {text_dict.get('my', '')}")
    line(out)


def button_row(out, label_en, label_my):
    line(out, f"  BUTTON  EN: {label_en}")
    line(out, f"          MY: {label_my}")


def L(out, label_key):
    """Look up a shared button label from keyboards._LABELS by key, to avoid the
    hardcoded strings below drifting out of sync with the actual code."""
    entry = keyboards._LABELS[label_key]
    button_row(out, entry["en"], entry["my"])


def main():
    out = []
    line(out, "EzyMap Algo Bot: All Messages & Buttons (English / Bahasa Melayu)")
    line(out, "Generated from ezymap_bot/content.py and keyboards.py, this is a reference")
    line(out, "copy; the bot itself always reads from the code, not this file.")

    # --- Welcome / language ---
    section(out, "1. /start: LANGUAGE SELECTION (shown first, bilingual, no toggle)")
    line(out, content.LANGUAGE_SELECT_TEXT)
    button_row(out, "🇬🇧 English", "🇲🇾 Bahasa Melayu")

    section(out, "2. WELCOME MESSAGES (sent after language is chosen, 3 messages)")
    for i, (en, my) in enumerate(zip(content.WELCOME_MESSAGES["en"], content.WELCOME_MESSAGES["my"]), start=1):
        bilingual(out, f"Welcome message {i}", {"en": en, "my": my})

    # --- Main menu ---
    section(out, "3. MAIN MENU")
    bilingual(out, "Main menu text", content.MAIN_MENU_TEXT)
    L(out, "check_out_free_steps")
    L(out, "purchase_ezymap")
    L(out, "why_choose_vantage")
    L(out, "faq")

    # --- Broker info ---
    section(out, "4. WHY CHOOSE VANTAGE (broker info screen)")
    bilingual(out, "Broker info text", content.BROKER_INFO_TEXT)
    L(out, "main_menu")

    # --- Packages ---
    section(out, "5. CHECK OUT FREE STEPS: package tier picker")
    bilingual(out, "Packages intro text", content.PACKAGES_INTRO_TEXT)
    tier_emoji = {"beginner": "🥉", "pro": "🥈", "premium": "🥇", "elite": "🏆"}
    for key in ("beginner", "pro", "premium", "elite"):
        tier = content.PACKAGE_TIERS[key]
        button_label = f"{tier_emoji[key]} {tier['name']}"
        button_row(out, button_label, f"{button_label} (name unchanged both languages)")
    line(out)
    line(out, "-- Tier detail screens --")
    for key in ("beginner", "pro", "premium", "elite"):
        tier = content.PACKAGE_TIERS[key]
        bilingual(out, f"{tier['name']} package detail", tier["detail"])
    line(out, "-- Buttons shown on every tier detail screen --")
    L(out, "open_new_account")
    L(out, "change_ib")
    L(out, "completed_registration")
    L(out, "back_to_packages")
    L(out, "main_menu")

    section(out, "6. OPEN NEW ACCOUNT")
    bilingual(out, "Open account text", content.OPEN_ACCOUNT_TEXT)
    L(out, "back")

    section(out, "7. CHANGE IB")
    bilingual(out, "Change IB text", content.CHANGE_IB_TEXT)
    L(out, "back")

    # --- Registration conversation ---
    section(out, "8. REGISTRATION FLOW (after tapping 'I've Completed Registration')")
    bilingual(out, "Ask for name", content.SUBMIT_DETAILS_PROMPT)
    bilingual(out, "Ask for email", content.ASK_EMAIL_TEXT)
    bilingual(out, "Ask for account number", content.ASK_ACCOUNT_TEXT)
    bilingual(out, "Ask for deposit proof (Pro/Premium/Elite only)", content.ASK_DEPOSIT_PROOF_TEXT)
    bilingual(out, "Submission confirmed (admin reached)", content.SUBMISSION_CONFIRMATION_TEXT)
    bilingual(out, "Submission confirmed (admin unreachable)", content.SUBMISSION_ADMIN_UNREACHABLE_TEXT)
    bilingual(out, "/cancel text", content.CANCEL_TEXT)

    # --- Purchase EzyMap ---
    section(out, "9. PURCHASE EZYMAP: category picker")
    bilingual(out, "Purchase intro text", content.PURCHASE_INTRO_TEXT)
    L(out, "tv_pro_category")
    L(out, "mt5_bundles_category")
    L(out, "main_menu")

    section(out, "10. MT5 - EZYMAP BUNDLES: product picker")
    bilingual(out, "MT5 bundles intro text", content.MT5_BUNDLES_INTRO_TEXT)
    for code in content.MT5_BUNDLE_PRODUCT_CODES:
        line(out, f"  BUTTON (same both languages): {content.PRODUCTS[code]['name']}")
    L(out, "back")
    L(out, "main_menu")

    section(out, "11. PRODUCT DETAIL SCREENS (TradingView Pro + each MT5 item)")
    for code, product in content.PRODUCTS.items():
        line(out, f"--- {product['name']} ---")
        bilingual(out, "Description", product["description"])
        line(out, "  Plan prices (same digits both languages, currency symbol only changes):")
        for duration in content.PLAN_DURATIONS:
            price = product["plans"][duration]
            en_label = content.plan_duration_label(duration, "en")
            my_label = content.plan_duration_label(duration, "my")
            line(out, f"    {en_label} (EN) / {my_label} (MY): ${price} USD  or  RM{price} MYR")
        if code == "tv_pro":
            button_row(out, "📊 Get TradingView FREE", "📊 Dapatkan TradingView PERCUMA")
        line(out)

    section(out, "12. CHOOSE PAYMENT METHOD (shown after picking a plan)")
    bilingual(out, "Choose payment method text (template)", content.CHOOSE_PAYMENT_METHOD_TEXT)
    L(out, "pay_usdt")
    L(out, "pay_xendit")
    L(out, "main_menu")

    section(out, "13. USDT PAYMENT PROMPT")
    bilingual(out, "USDT payment prompt (template, always priced in USD)", content.PAYMENT_PROMPT_TEMPLATE)
    L(out, "different_payment_method")
    L(out, "main_menu")
    bilingual(out, "USDT proof received (admin reached)", content.PAYMENT_PROOF_RECEIVED_TEXT)
    bilingual(out, "USDT proof received (admin unreachable)", content.PAYMENT_PROOF_ADMIN_UNREACHABLE_TEXT)

    section(out, "14. XENDIT (CARD/BANK/E-WALLET) PAYMENT")
    bilingual(out, "Xendit not set up yet", content.XENDIT_UNAVAILABLE_TEXT)
    bilingual(out, "Xendit invoice created (template)", content.XENDIT_INVOICE_CREATED_TEXT)
    L(out, "pay_now")
    L(out, "main_menu")
    bilingual(out, "Xendit invoice creation failed", content.XENDIT_INVOICE_FAILED_TEXT)
    bilingual(out, "Xendit payment auto-confirmed (sent to client)", content.XENDIT_AUTO_CONFIRM_CLIENT_TEXT)

    section(out, "15. FAQ")
    line(out, "List header:")
    bilingual(out, "FAQ list header", content.FAQ_LIST_HEADER)
    for i, item in enumerate(content.FAQ_ITEMS):
        line(out, f"--- FAQ #{i + 1} ---")
        bilingual(out, "Question", item["question"])
        bilingual(out, "Answer", item["answer"])
        if item["extra_button"]:
            button_row(out, item["extra_button"]["label"]["en"], item["extra_button"]["label"]["my"])
        if item["show_contact_admin"]:
            L(out, "contact_admin")
        L(out, "back_to_faq")
        line(out)

    section(out, "16. ADMIN-ONLY NOTIFICATIONS (always English, sent to Jack, not the client)")
    line(out, "These are not shown to clients at all, so no Malay version exists:")
    line(out, "- New registration submission: Package / Name / Email / Account Number / Telegram")
    line(out, "  username / Telegram ID / (Deposit proof forwarded below, if applicable)")
    line(out, "- New payment proof (USDT): Product / Plan / Telegram username / Telegram ID")
    line(out, "- Payment confirmed via Xendit: Product / Plan / Telegram username / Telegram ID")
    line(out, "- Every admin notification includes a 'Chat with Client' button")

    output_path = sys.argv[1] if len(sys.argv) > 1 else "ezymap_bot_messages_reference.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
