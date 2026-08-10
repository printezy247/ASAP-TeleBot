# ASAP-TeleBot

A button-driven Telegram registration bot for **A$AP USD**. It replaces the manual
registration channel: clients tap through open-account / change-IB / deposit / withdraw
instructions themselves, and only reach your (admin) DM once they submit their final
Name / Email / Account Number — cutting out the repeated back-and-forth.

## Flow

1. `/start` — three welcome messages (intro, risk reminder, ready-to-go) followed by the
   main menu.
2. **Main menu** — Get My Free Signals / Learn More About Broker / FAQ.
3. **Get My Free Signals** — explains that VIP access requires an account opened (or IB
   changed) under your IB, no deposit required, then offers:
   - Open New Account (step-by-step, with your IB link)
   - Change IB (step-by-step, with your IB link/number)
   - Deposit (bank / card / BTC / USDT sub-guides)
   - Withdraw (verification + limits)
   - ✅ I've Completed Registration — starts a short conversation (Name → Email →
     Account Number) and forwards the submission straight to your admin DM.
4. **FAQ** — common questions answered instantly via buttons, so your sales admin stops
   getting asked the same things.

## Setup

1. Install dependencies (Python 3.11+ recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in your values:

   ```bash
   cp .env.example .env
   ```

   - `BOT_TOKEN` — from [@BotFather](https://t.me/BotFather).
   - `ADMIN_CHAT_ID` — your numeric Telegram chat ID (get it from
     [@userinfobot](https://t.me/userinfobot)). Registration submissions are DM'd here.

   `.env` is gitignored — never commit real credentials.

3. Run the bot:

   ```bash
   python -m asap_telebot.main
   ```

   This uses long polling, so it just needs to run on any always-on machine (a small VPS,
   a $5/mo box, or a background process on your own server) — no public URL or webhook
   setup required.

## Editing content

All bot copy (welcome messages, broker links, deposit/withdraw guides, FAQ) lives in
`asap_telebot/content.py`. Update the constants there (e.g. `OPEN_ACCOUNT_LINK`,
`CHANGE_IB_LINK`, `IB_NUMBER`, `FAQ_ITEMS`) as your links or offers change — no need to
touch the handler logic.

## Project layout

```
asap_telebot/
  config.py        # loads BOT_TOKEN / ADMIN_CHAT_ID from .env
  content.py        # all bot copy — edit this to change wording/links
  keyboards.py       # inline button layouts
  main.py            # wires handlers together, starts polling
  handlers/
    start.py         # /start welcome + main menu
    menu.py           # button navigation (broker info, FAQ, deposit guides, etc.)
    registration.py    # Name/Email/Account Number conversation -> admin DM
```

## Security note

If your bot token is ever pasted into a chat, doc, or committed to git, treat it as
compromised: regenerate it via `@BotFather` → `/mytoken` → `/revoke`, then update `.env`.
