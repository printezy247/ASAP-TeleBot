import httpx

from .config import XENDIT_SECRET_KEY

XENDIT_INVOICE_URL = "https://api.xendit.co/v2/invoices"


async def create_invoice(
    *, external_id: str, amount: float, currency: str, description: str
) -> dict:
    """Create a Xendit Invoice and return the parsed JSON response (includes
    'invoice_url' to send the client, and 'id' as Xendit's own invoice ID).
    Raises httpx.HTTPStatusError on failure - callers should catch it.
    """
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            XENDIT_INVOICE_URL,
            auth=(XENDIT_SECRET_KEY, ""),
            json={
                "external_id": external_id,
                "amount": amount,
                "currency": currency,
                "description": description,
            },
        )
        response.raise_for_status()
        return response.json()
