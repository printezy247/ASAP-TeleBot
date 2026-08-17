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

For **EzyMap Algo** (ambassador Jack, broker Vantage Markets). Four free package tiers
unlocked by broker account status under Jack's IB:

- 🥉 **Beginner** — open an account under the IB (no deposit) → free eBooks + EzyMap Lite
  indicator.
- 🥈 **Pro** — account + any deposit → EzyMap Scalp Mastery signals channel + Beginner perks.
- 🥇 **Premium** — account + min $100 deposit → EzyMap Pro indicator with live M1–H4
  signals + Pro perks.
- 🏆 **Elite** — account + min $700 deposit → full EzyMap MT5 indicator set + private
  1-on-1 support group + Premium perks.

Plus a separate **paid catalog**, *Purchase EzyMap* (TradingView - EzyMap Pro, and the
MT5 indicator bundle/individual tools): client picks a product and plan, then pays via
**USDT** — wallet address + network instructions; client sends a screenshot or
transaction ID, which is forwarded to Jack (with the original message/photo) for review.
(USDT is the only payment method right now; more are planned later — see
`payment_method_menu()` in `ezymap_bot/keyboards.py`, which is kept as its own screen for
exactly that reason.)

Both this and free-tier registrations end the same way: an admin notification with
**✅ Approve / ❌ Reject** buttons right on the message, so Jack can act without leaving
the chat — tapping one immediately messages the client back ("your package has been
approved!" / "your payment is confirmed!"). See [Admin approvals](#admin-approvals) below.

1. `/start` → welcome messages → main menu: **Check Out FREE Steps**, **Purchase EzyMap**,
   **Why Choose Vantage**, **FAQ**.
2. **Check Out FREE Steps** — explains the four tiers, then Open New Account / Change IB
   (done by email, not a link — the bot gives you the exact email template to send) /
   ✅ I've Completed Registration (Name → Email → Account Number → deposit proof screenshot
   for Pro/Premium/Elite → Jack's DM with Approve/Reject).
3. **Purchase EzyMap** — pick TradingView or an MT5 bundle/tool, then a plan → USDT
   payment instructions → proof → Jack's DM with Approve/Reject.
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
there polling, and free accounts get exactly **one** web app.

Since both bots need to run somewhere, **`combined_webhook_app.py`** serves both from
that single web app — each bot keeps its own URL route and its own secret, so from
Telegram's point of view they're completely independent; they just happen to share one
PythonAnywhere process. (Hosting location and admin identity are unrelated — Jack
doesn't need his own PythonAnywhere account just to receive DMs.)

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
   nano .env   # fill in BOTH bots' values: BOT_TOKEN/ADMIN_CHAT_ID/WEBHOOK_SECRET
               # AND EZYMAP_BOT_TOKEN/EZYMAP_ADMIN_CHAT_ID/EZYMAP_WEBHOOK_SECRET
   ```
3. Go to the **Web** tab → **Add a new web app** → choose **Flask** → Python 3.11 (match
   whatever `python3.11 -m venv` used above — check the Python version shown on the Web
   tab and use the matching `python3.X` command if it's not 3.11).
4. Click the **WSGI configuration file** link and replace the bottom of it with:
   ```python
   import sys
   path = '/home/<your-pythonanywhere-username>/ASAP-TeleBot'
   if path not in sys.path:
       sys.path.insert(0, path)

   from combined_webhook_app import app as application
   ```
5. Under the web app's **Virtualenv** section, point it at
   `/home/<your-pythonanywhere-username>/ASAP-TeleBot/.venv`.
6. Click the green **Reload** button on the Web tab.
7. Tell Telegram where to send updates for **each** bot (two separate calls, run once
   each from the Bash console):
   ```bash
   curl "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://<your-pythonanywhere-username>.pythonanywhere.com/webhook/asap/<WEBHOOK_SECRET>"
   curl "https://api.telegram.org/bot<EZYMAP_BOT_TOKEN>/setWebhook?url=https://<your-pythonanywhere-username>.pythonanywhere.com/webhook/ezymap/<EZYMAP_WEBHOOK_SECRET>"
   ```

That's it — both bots now run permanently on the same PythonAnywhere web app, no
laptop or terminal required, no paid plan needed. To push future code updates: open a
Bash console, `cd ASAP-TeleBot && git pull`, then hit **Reload** on the Web tab again.

If you'd still rather keep the bots on fully separate hosts (e.g. `asap_telebot` on
your account, `ezymap_bot` on a second free account under a different email), the
per-bot `webhook_app.py` files still work individually — just import from
`asap_telebot.webhook_app` or `ezymap_bot.webhook_app` instead of
`combined_webhook_app` in step 4, and only set that one bot's webhook in step 7.

**Keeping it alive:** PythonAnywhere free sites need a login + click **"Run until 1 month
from today"** (on the Web tab) at least once a month, or the site gets disabled. They
email a reminder a week ahead.

## Admin approvals

Both of `ezymap_bot`'s submission flows (free-tier registration and USDT payment proof)
end with an admin DM carrying **✅ Approve** and **❌ Reject** buttons, plus a
**💬 Chat with Client** link. Tapping Approve or Reject:

- Immediately messages the client back in their original chat (a localized "your
  package has been approved!" / "your payment is confirmed!" message, or a polite
  "couldn't verify this time" message on reject).
- Replaces the button row on the admin's own message with a plain "✅ Approved" /
  "❌ Rejected" label, so it's obvious at a glance which notifications are still pending.

Pending submissions are tracked in `bot_data` (the same `PicklePersistence` file
everything else uses), keyed by a short random ID kept out of the button's
`callback_data` — so unlike a purely in-memory store, they survive a bot restart. Tapping
Approve/Reject on a submission that's already been resolved (or whose record predates the
persistence file, e.g. right after wiping it) just tells Jack it's already been handled.

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
  submission_store.py  # tracks pending registrations/payments awaiting admin Approve/Reject
  handlers/
    start.py, menu.py, registration.py   # same roles as above
    payment.py          # USDT payment prompt -> proof (photo/text) -> admin DM
    decision.py          # handles the admin's Approve/Reject tap -> notifies the client
```

## Security note

If a bot token is ever pasted into a chat, doc, or committed to git, treat it as
compromised: regenerate it via `@BotFather` → `/mytoken` → `/revoke`, then update `.env`.
