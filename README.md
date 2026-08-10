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

   This uses long polling — it only responds while this process is running. Fine for
   testing on your own computer, but it stops the moment you close the terminal.

## Running it 24/7 for free (no credit card)

For real client registrations you need the bot running somewhere always-on — not your
laptop. [PythonAnywhere](https://www.pythonanywhere.com/) offers a free tier that never
asks for a credit card and never sleeps, but it hosts *web apps*, not scripts that sit
there polling. So instead of `python -m asap_telebot.main`, deploy `webhook_app.py`,
which makes Telegram push updates to a URL instead of the bot asking for them.

1. Sign up free at pythonanywhere.com (no card required).
2. Open a **Bash console** from your PythonAnywhere dashboard and run:
   ```bash
   git clone https://github.com/printezy247/ASAP-TeleBot.git
   cd ASAP-TeleBot
   git checkout claude/telegram-registration-bot-qo6cq8
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   nano .env   # fill in BOT_TOKEN, ADMIN_CHAT_ID, and a random WEBHOOK_SECRET
   ```
3. Go to the **Web** tab → **Add a new web app** → choose **Flask** → Python 3.11 (or
   closest available).
4. In that web app's config, set the **source code** / **working directory** to
   `/home/<your-pythonanywhere-username>/ASAP-TeleBot`, and edit the auto-generated
   `WSGI configuration file` so the bottom of it reads:
   ```python
   import sys
   path = '/home/<your-pythonanywhere-username>/ASAP-TeleBot'
   if path not in sys.path:
       sys.path.insert(0, path)

   from asap_telebot.webhook_app import app as application
   ```
5. Under the web app's **Virtualenv** section, point it at
   `/home/<your-pythonanywhere-username>/ASAP-TeleBot/.venv`.
6. Click the green **Reload** button on the Web tab.
7. Tell Telegram where to send updates (replace the placeholders, run once from the
   Bash console):
   ```bash
   curl "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://<your-pythonanywhere-username>.pythonanywhere.com/webhook/<WEBHOOK_SECRET>"
   ```

That's it — the bot now runs permanently on PythonAnywhere's servers, no laptop or
terminal required. To push future code updates: open a Bash console,
`cd ASAP-TeleBot && git pull`, then hit **Reload** on the Web tab again.

## Editing content

All bot copy (welcome messages, broker links, deposit/withdraw guides, FAQ) lives in
`asap_telebot/content.py`. Update the constants there (e.g. `OPEN_ACCOUNT_LINK`,
`CHANGE_IB_LINK`, `IB_NUMBER`, `FAQ_ITEMS`) as your links or offers change — no need to
touch the handler logic.

## Project layout

```
asap_telebot/
  config.py        # loads BOT_TOKEN / ADMIN_CHAT_ID / etc. from .env
  content.py        # all bot copy — edit this to change wording/links
  keyboards.py       # inline button layouts
  main.py            # wires handlers together; run directly for local polling mode
  webhook_app.py      # Flask entry point for free webhook hosting (e.g. PythonAnywhere)
  handlers/
    start.py         # /start welcome + main menu
    menu.py           # button navigation (broker info, FAQ, deposit guides, etc.)
    registration.py    # Name/Email/Account Number conversation -> admin DM
```

## Security note

If your bot token is ever pasted into a chat, doc, or committed to git, treat it as
compromised: regenerate it via `@BotFather` → `/mytoken` → `/revoke`, then update `.env`.
