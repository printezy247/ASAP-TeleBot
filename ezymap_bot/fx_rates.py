"""Live USD -> any-currency exchange rates, used only to show a realistic localized
price while browsing the catalog - see format_price() in content.py. Actual USDT/card
payments always stay quoted in USD (crypto has no native local-currency price, see the
note on PAYMENT_PROMPT_TEMPLATE in content.py), so a stale or unreachable rate here
never affects what anyone is actually charged.

Pulls the full rates table (~160 ISO currency codes) from a free, keyless FX API in one
shot, rather than a handful of hardcoded currencies, so clients anywhere in the world
can see their own local price - not just a handful of pre-picked countries.

Rates are cached in memory (this module's globals persist for the life of the WSGI
worker process, even though a fresh PTB Application is built per webhook request) and
refreshed at most once every few hours, so browsing the catalog doesn't hit the network
on every button tap. If a refresh ever fails, the last good rates keep being used - or,
on a completely fresh process that's never fetched successfully, a small fixed fallback
covering just the currencies most likely to matter until the next successful refresh.
"""

import logging
import time

import httpx

logger = logging.getLogger(__name__)

FX_API_URL = "https://open.er-api.com/v6/latest/USD"
_CACHE_TTL_SECONDS = 12 * 60 * 60  # refresh at most twice a day

# Only used before the very first successful fetch on a fresh process. Rough,
# occasionally-stale figures here are far better than an error shown to the client.
_FALLBACK_RATES = {"myr": 4.7, "idr": 16300.0, "bnd": 1.34, "sgd": 1.34, "eur": 0.92, "gbp": 0.79, "aud": 1.52}

_cache = {"rates": None, "fetched_at": 0.0}


def _refresh_if_stale() -> None:
    if _cache["rates"] is not None and (time.time() - _cache["fetched_at"]) < _CACHE_TTL_SECONDS:
        return
    try:
        response = httpx.get(FX_API_URL, timeout=10)
        response.raise_for_status()
        rates = response.json()["rates"]
        _cache["rates"] = {code.lower(): rate for code, rate in rates.items()}
        _cache["fetched_at"] = time.time()
    except (httpx.HTTPError, KeyError, ValueError, TypeError):
        logger.exception(
            "Failed to refresh FX rates, falling back to %s rates",
            "cached" if _cache["rates"] else "fixed fallback",
        )


def _rates() -> dict:
    _refresh_if_stale()
    return _cache["rates"] or _FALLBACK_RATES


def is_known_currency(currency: str) -> bool:
    return currency.lower() in _rates()


def usd_to(currency: str, usd_amount: float):
    """Converts a USD amount to any recognized ISO currency code. Returns None (not
    an exception) if the code isn't recognized, so callers can fall back to USD.
    """
    rate = _rates().get(currency.lower())
    return usd_amount * rate if rate is not None else None
