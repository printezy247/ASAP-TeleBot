"""Generates simple PNG receipt/confirmation images sent to clients (and Jack) when
a free package registration, USDT payment, or Telegram Payments purchase completes.

No external assets required beyond the two bundled DejaVu font files - this keeps
image generation self-contained and independent of whatever fonts happen to be
installed on the host (important since this runs on PythonAnywhere).
"""

import io
import os
from datetime import datetime, timezone

from PIL import Image, ImageDraw, ImageFont

_FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "fonts")
_REGULAR_FONT_PATH = os.path.join(_FONT_DIR, "DejaVuSans.ttf")
_BOLD_FONT_PATH = os.path.join(_FONT_DIR, "DejaVuSans-Bold.ttf")

_WIDTH = 900
_MARGIN = 48
_CARD_PADDING = 40

_BG_COLOR = (241, 243, 245)
_CARD_COLOR = (255, 255, 255)
_BORDER_COLOR = (225, 228, 232)
_TEXT_PRIMARY = (30, 33, 36)
_TEXT_SECONDARY = (110, 118, 125)
_ACCENT_COLOR = (16, 124, 65)  # green, matches a "confirmed/paid" tone
_DIVIDER_COLOR = (232, 234, 237)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(_BOLD_FONT_PATH if bold else _REGULAR_FONT_PATH, size)


def _text_height(draw: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont) -> int:
    bbox = draw.textbbox((0, 0), "Ag", font=font)
    return bbox[3] - bbox[1]


def build_receipt_png(
    *,
    kicker: str,
    title: str,
    big_line: str,
    subtitle: str,
    rows: list[tuple[str, str]],
    footer: str,
) -> bytes:
    """Renders a single-card receipt. `rows` is a list of (label, value) pairs."""
    row_height = 56
    height = (
        _MARGIN * 2
        + _CARD_PADDING * 2
        + 40  # kicker
        + 56  # title
        + 70  # big_line
        + 36  # subtitle
        + 30  # spacing before divider
        + len(rows) * row_height
        + 40  # spacing before footer
        + 30  # footer
    )

    img = Image.new("RGB", (_WIDTH, height), _BG_COLOR)
    draw = ImageDraw.Draw(img)

    card_x0, card_y0 = _MARGIN, _MARGIN
    card_x1, card_y1 = _WIDTH - _MARGIN, height - _MARGIN
    draw.rounded_rectangle(
        [card_x0, card_y0, card_x1, card_y1], radius=20, fill=_CARD_COLOR, outline=_BORDER_COLOR, width=1
    )

    x = card_x0 + _CARD_PADDING
    y = card_y0 + _CARD_PADDING

    kicker_font = _font(20, bold=True)
    draw.text((x, y), kicker.upper(), font=kicker_font, fill=_ACCENT_COLOR)
    y += _text_height(draw, kicker_font) + 14

    title_font = _font(34, bold=True)
    draw.text((x, y), title, font=title_font, fill=_TEXT_PRIMARY)
    y += _text_height(draw, title_font) + 18

    big_font = _font(46, bold=True)
    draw.text((x, y), big_line, font=big_font, fill=_TEXT_PRIMARY)
    y += _text_height(draw, big_font) + 12

    subtitle_font = _font(22)
    draw.text((x, y), subtitle, font=subtitle_font, fill=_TEXT_SECONDARY)
    y += _text_height(draw, subtitle_font) + 28

    draw.line([(x, y), (card_x1 - _CARD_PADDING, y)], fill=_DIVIDER_COLOR, width=2)
    y += 24

    label_font = _font(22)
    value_font = _font(22, bold=True)
    for label, value in rows:
        draw.text((x, y), label, font=label_font, fill=_TEXT_SECONDARY)
        value_width = draw.textlength(value, font=value_font)
        draw.text((card_x1 - _CARD_PADDING - value_width, y), value, font=value_font, fill=_TEXT_PRIMARY)
        y += row_height

    y += 12
    draw.line([(x, y), (card_x1 - _CARD_PADDING, y)], fill=_DIVIDER_COLOR, width=2)
    y += 24

    footer_font = _font(18)
    draw.text((x, y), footer, font=footer_font, fill=_TEXT_SECONDARY)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()


def _today(region: str) -> str:
    now = datetime.now(timezone.utc)
    if region == "my":
        return now.strftime("%d %b %Y")
    return now.strftime("%B %d, %Y")


def registration_receipt(*, name: str, package_name: str, region: str) -> bytes:
    if region == "my":
        return build_receipt_png(
            kicker="EzyMap Algo",
            title="Pendaftaran Disahkan",
            big_line=package_name,
            subtitle=f"Disahkan {_today(region)}",
            rows=[("Nama", name), ("Pakej", package_name)],
            footer="Ada soalan? Mesej Jack di Telegram.",
        )
    return build_receipt_png(
        kicker="EzyMap Algo",
        title="Registration Confirmed",
        big_line=package_name,
        subtitle=f"Confirmed {_today(region)}",
        rows=[("Name", name), ("Package", package_name)],
        footer="Questions? Message Jack on Telegram.",
    )


def payment_receipt(
    *,
    product_name: str,
    plan_name: str,
    price: str,
    currency_symbol: str,
    payment_method: str,
    receipt_number: str,
    region: str,
) -> bytes:
    amount = f"{currency_symbol}{price}"
    if region == "my":
        return build_receipt_png(
            kicker="EzyMap Algo",
            title="Resit Pembayaran",
            big_line=amount,
            subtitle=f"Dibayar {_today(region)}",
            rows=[
                ("No. Resit", receipt_number),
                ("Produk", product_name),
                ("Pelan", plan_name),
                ("Kaedah Bayaran", payment_method),
            ],
            footer="Ada soalan? Mesej Jack di Telegram.",
        )
    return build_receipt_png(
        kicker="EzyMap Algo",
        title="Payment Receipt",
        big_line=amount,
        subtitle=f"Paid {_today(region)}",
        rows=[
            ("Receipt No.", receipt_number),
            ("Product", product_name),
            ("Plan", plan_name),
            ("Payment Method", payment_method),
        ],
        footer="Questions? Message Jack on Telegram.",
    )
