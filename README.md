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
MT5 indicator bundle/individual tools): client picks a product and plan, then chooses how
to pay:
- **USDT** — wallet address + network instructions; client sends a screenshot or
  transaction ID, which is forwarded to Jack (with the original message/photo) for manual
  confirmation.
- **Xendit** (card/bank transfer/e-wallet) — the bot creates a Xendit invoice and sends
  the client a "Pay Now" link; once Xendit confirms the payment via webhook, both Jack and
  the client are notified automatically — no manual confirmation needed. Falls back to a
  friendly "not set up yet" message (pointing the client to USDT instead) if the Xendit
  API keys aren't configured, or if invoice creation fails.

1. `/start` → welcome messages → main menu: **Check Out FREE Steps**, **Purchase EzyMap**,
   **Why Choose Vantage**, **FAQ**.
2. **Check Out FREE Steps** — explains the four tiers, then Open New Account / Change IB
   (done by email, not a link — the bot gives you the exact email template to send) /
   ✅ I've Completed Registration (Name → Email → Account Number → deposit proof screenshot
   for Pro/Premium/Elite → Jack's DM).
3. **Purchase EzyMap** — pick TradingView or an MT5 bundle/tool, then a plan → choose
   USDT or Xendit → payment instructions/link → confirmation (manual for USDT, automatic
   for Xendit).
4. **FAQ** — includes a "What if I get stuck?" / "cancel/refund" entry with a Contact
   Admin button.

Before this one can run, fill in `ezymap_bot/content.py`:
- `USDT_WALLET_ADDRESS` — currently a placeholder, replace with your real wallet address.
- `USDT_NETWORK` — defaults to `TRC20`, change if you use a different network.

Xendit is optional — see [Xendit setup](#xendit-setup-optional) below. Without it
configured, the Xendit button still shows but tells the client to use USDT instead.

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
   - `EZYMAP_XENDIT_SECRET_KEY` / `EZYMAP_XENDIT_CALLBACK_TOKEN` — optional, only needed
     for the Xendit (card/bank/e-wallet) payment option. See
     [Xendit setup](#xendit-setup-optional) below. Leave blank to only offer USDT.

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

If you filled in `EZYMAP_XENDIT_SECRET_KEY`, also register the Xendit callback URL —
see [Xendit setup](#xendit-setup-optional) below — otherwise Xendit invoices will get
created but payments will never auto-confirm.

If you'd still rather keep the bots on fully separate hosts (e.g. `asap_telebot` on
your account, `ezymap_bot` on a second free account under a different email), the
per-bot `webhook_app.py` files still work individually — just import from
`asap_telebot.webhook_app` or `ezymap_bot.webhook_app` instead of
`combined_webhook_app` in step 4, and only set that one bot's webhook in step 7.

**Keeping it alive:** PythonAnywhere free sites need a login + click **"Run until 1 month
from today"** (on the Web tab) at least once a month, or the site gets disabled. They
email a reminder a week ahead.

## Xendit setup (optional)

Lets `ezymap_bot` clients pay for *Purchase EzyMap* items by card, bank transfer, or
e-wallet instead of USDT, with automatic confirmation. Skip this entirely and the bot
just offers USDT — nothing else breaks.

1. Sign up at [xendit.co](https://dashboard.xendit.co/register) and get your **Secret API
   Key** from **Settings → API Keys** → put it in `.env` as `EZYMAP_XENDIT_SECRET_KEY`.
   Use a test-mode key first if you want to try it before going live.
2. In the dashboard, go to **Settings → Webhooks** and add a callback for the **Invoice
   Paid** event, pointing at wherever this app is hosted:
   - Combined app (`combined_webhook_app.py`): `https://<your-host>/xendit/webhook/ezymap`
   - Standalone `ezymap_bot/webhook_app.py`: `https://<your-host>/xendit/webhook`
3. Copy the **Verification Token** shown on that same Webhooks page into `.env` as
   `EZYMAP_XENDIT_CALLBACK_TOKEN` — this is how the app confirms a callback really came
   from Xendit (checked against the `x-callback-token` header on every request).
4. Reload/restart the app so it picks up the new `.env` values.
5. Confirm your Xendit account's supported invoice currencies include both `USD` and
   `MYR` (the two currencies this bot requests, based on the client's chosen language) —
   check **Settings → Business** in the dashboard, or ask Xendit support if unsure.

Until steps 1–3 are done, the "Pay with Card/Bank/E-Wallet" button shows a friendly
"not set up yet" message and points the client to USDT instead — the rest of the bot is
unaffected either way.

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
    payment.py          # USDT payment prompt -> proof (photo/text) -> admin DM
    xendit_payment.py    # creates a Xendit invoice, sends the client the pay link
  xendit_client.py      # thin wrapper around the Xendit Invoice API (httpx)
  xendit_webhook.py      # handles Xendit's "invoice paid" callback -> notifies admin+client
  invoice_store.py        # JSON file mapping a Xendit invoice's external_id -> Telegram chat/product
```

## Security note

If a bot token is ever pasted into a chat, doc, or committed to git, treat it as
compromised: regenerate it via `@BotFather` → `/mytoken` → `/revoke`, then update `.env`.
