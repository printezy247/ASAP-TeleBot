# ASAP-TeleBot

Two button-driven Telegram registration bots, each replacing a manual registration
channel: clients tap through instructions themselves, and only reach the admin's DM once
they submit final details (or payment proof) — cutting out repeated back-and-forth.

- **`asap_telebot/`** — for **A$AP USD** (Elev8 broker). See [Flow](#flow) below.
- **`ezymap_bot/`** — for **EzyMap Algo** (Vantage Markets broker), with tiered package
  perks plus a paid EzyMap Pro subscription. See [EzyMap Algo bot](#ezymap-algo-bot) below.

## Flow (asap_telebot)

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

## EzyMap Algo bot

For **EzyMap Algo** (ambassador Jack, broker Vantage Markets). Three free package tiers
unlocked by broker account status under Jack's IB:

- 🥉 **Beginner** — open an account under the IB (no deposit) → free eBooks + EzyMap Lite
  indicator.
- 🥈 **Pro** — account + any deposit → EzyMap Scalp Mastery signals channel + Beginner perks.
- 🥇 **Premium** — account + min $100 deposit → EzyMap Pro indicator with live M1–H4
  signals + Pro perks.

Plus a separate **paid subscription**, EzyMap Pro ($29/month, $149/6 months, $249/year):
client picks a plan, gets a USDT wallet address + instructions, sends a screenshot or
transaction ID, which is forwarded to Jack (with the original message/photo) for manual
confirmation — no automatic payment verification.

1. `/start` → welcome messages → main menu: **See Packages / Join**, **Get EzyMap Pro**,
   **Learn More About Broker**, **FAQ**.
2. **See Packages / Join** — explains the three tiers, then Open New Account / Change IB
   (done by email, not a link — the bot gives you the exact email template to send) /
   ✅ I've Completed Registration (Name → Email → Account Number → Jack's DM).
3. **Get EzyMap Pro** — pick a plan → USDT payment instructions → send proof (photo or
   text) → forwarded to Jack with a "Chat with Client" button.
4. **FAQ** — includes a "What if I get stuck?" / "cancel/refund" entry with a Contact
   Admin button.

Before this one can run, fill in `ezymap_bot/content.py`:
- `USDT_WALLET_ADDRESS` — currently a placeholder, replace with your real wallet address.
- `USDT_NETWORK` — defaults to `TRC20`, change if you use a different network.

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

   For `asap_telebot`:
   - `BOT_TOKEN` — from [@BotFather](https://t.me/BotFather).
   - `ADMIN_CHAT_ID` — your numeric Telegram chat ID (get it from
     [@userinfobot](https://t.me/userinfobot)). Registration submissions are DM'd here.

   For `ezymap_bot` (create a **second, separate bot** with @BotFather — don't reuse the
   same token):
   - `EZYMAP_BOT_TOKEN` — token for the second bot.
   - `EZYMAP_ADMIN_CHAT_ID` — Jack's numeric Telegram chat ID.

   `.env` is gitignored — never commit real credentials.

3. Run a bot locally:

   ```bash
   python -m asap_telebot.main
   # or
   python -m ezymap_bot.main
   ```

   This uses long polling — it only responds while this process is running. Fine for
   testing on your own computer, but it stops the moment you close the terminal.

## Running it 24/7 for free (no credit card)

For real client registrations you need the bot running somewhere always-on — not your
laptop. [PythonAnywhere](https://www.pythonanywhere.com/) offers a free tier that never
asks for a credit card and never sleeps, but it hosts *web apps*, not scripts that sit
there polling. So instead of `python -m asap_telebot.main`, deploy `webhook_app.py`,
which makes Telegram push updates to a URL instead of the bot asking for them.

> **Free accounts are limited to one web app each.** Since `ezymap_bot` has a different
> admin (Jack) anyway, the simplest setup is: you keep `asap_telebot` on your
> PythonAnywhere account, and Jack signs up for his own free PythonAnywhere account and
> hosts `ezymap_bot` there (same steps below, just his own account/credentials). Both
> bots live in this same GitHub repo either way.

1. Sign up free at pythonanywhere.com (no card required).
2. Open a **Bash console** from the PythonAnywhere dashboard and run:
   ```bash
   git clone https://github.com/printezy247/ASAP-TeleBot.git
   cd ASAP-TeleBot
   git checkout claude/telegram-registration-bot-qo6cq8
   python3.11 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   nano .env   # fill in BOT_TOKEN/ADMIN_CHAT_ID/WEBHOOK_SECRET, or the EZYMAP_ ones
   ```
3. Go to the **Web** tab → **Add a new web app** → choose **Flask** → Python 3.11 (match
   whatever `python3.11 -m venv` used above — check the Python version shown on the Web
   tab and use the matching `python3.X` command if it's not 3.11).
4. In that web app's config, edit the auto-generated **WSGI configuration file** so the
   bottom of it reads (for `asap_telebot`):
   ```python
   import sys
   path = '/home/<your-pythonanywhere-username>/ASAP-TeleBot'
   if path not in sys.path:
       sys.path.insert(0, path)

   from asap_telebot.webhook_app import app as application
   ```
   For `ezymap_bot`, use `from ezymap_bot.webhook_app import app as application` instead.
5. Under the web app's **Virtualenv** section, point it at
   `/home/<your-pythonanywhere-username>/ASAP-TeleBot/.venv`.
6. Click the green **Reload** button on the Web tab.
7. Tell Telegram where to send updates (replace the placeholders, run once from the
   Bash console):
   ```bash
   curl "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://<your-pythonanywhere-username>.pythonanywhere.com/webhook/<WEBHOOK_SECRET>"
   ```
   Use `EZYMAP_BOT_TOKEN`/`EZYMAP_WEBHOOK_SECRET` values for the `ezymap_bot` deployment.

That's it — the bot now runs permanently on PythonAnywhere's servers, no laptop or
terminal required. To push future code updates: open a Bash console,
`cd ASAP-TeleBot && git pull`, then hit **Reload** on the Web tab again.

**Keeping it alive:** PythonAnywhere free sites need a login + click **"Run until 1 month
from today"** (on the Web tab) at least once a month, or the site gets disabled. They
email a reminder a week ahead.

## Editing content

All bot copy (welcome messages, broker links, package perks, FAQ, payment details) lives
in `asap_telebot/content.py` and `ezymap_bot/content.py` respectively. Update the
constants there as your links, offers, or pricing change — no need to touch the handler
logic.

## Project layout

```
asap_telebot/       # A$AP USD bot (Elev8 broker)
  config.py          # loads BOT_TOKEN / ADMIN_CHAT_ID / etc. from .env
  content.py          # all bot copy — edit this to change wording/links
  keyboards.py         # inline button layouts
  main.py              # wires handlers together; run directly for local polling mode
  webhook_app.py        # Flask entry point for free webhook hosting (e.g. PythonAnywhere)
  handlers/
    start.py           # /start welcome + main menu
    menu.py             # button navigation (broker info, FAQ, deposit guides, etc.)
    registration.py      # Name/Email/Account Number conversation -> admin DM

ezymap_bot/         # EzyMap Algo bot (Vantage Markets broker)
  config.py, content.py, keyboards.py, main.py, webhook_app.py   # same roles as above
  handlers/
    start.py, menu.py, registration.py   # same roles as above
    payment.py          # EzyMap Pro plan selection -> USDT payment proof -> admin DM
```

## Security note

If a bot token is ever pasted into a chat, doc, or committed to git, treat it as
compromised: regenerate it via `@BotFather` → `/mytoken` → `/revoke`, then update `.env`.
