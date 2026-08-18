import httpx

from .config import NOWPAYMENTS_API_KEY

NOWPAYMENTS_INVOICE_URL = "https://api.nowpayments.io/v1/invoice"

# Where NOWPayments' hosted checkout page sends the client back to after paying (or
# cancelling) - there's no web app of ours to land on, so both just point at the bot
# itself. NOWPayments requires both fields even though we don't use them for anything.
RETURN_URL = "https://t.me/ezyregisterbot"


async def create_invoice(
    *, order_id: str, amount: float, description: str, ipn_callback_url: str
) -> dict:
    """Create a NOWPayments Invoice and return the parsed JSON response (includes
    'invoice_url' to send the client). Always priced in USD - see the matching note on
    PAYMENT_PROMPT_TEMPLATE in content.py for why USDT/card payments ignore the
    client's chosen display currency. Raises httpx.HTTPStatusError on failure - callers
    should catch it.
    """
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            NOWPAYMENTS_INVOICE_URL,
            headers={"x-api-key": NOWPAYMENTS_API_KEY},
            json={
                "price_amount": amount,
                "price_currency": "usd",
                "order_id": order_id,
                "order_description": description,
                "ipn_callback_url": ipn_callback_url,
                "success_url": RETURN_URL,
                "cancel_url": RETURN_URL,
            },
        )
        response.raise_for_status()
        return response.json()
