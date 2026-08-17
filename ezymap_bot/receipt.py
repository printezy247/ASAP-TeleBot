"""Generates a branded PNG receipt card (like a digital confirmation slip) for a
client the moment their registration or payment is approved. Sent as a photo
alongside the usual confirmation text - see handlers/decision.py.
"""

import io
import os
from datetime import datetime

from PIL import Image, ImageDraw, ImageFilter, ImageFont

_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
_FONT_DIR = os.path.join(_MODULE_DIR, "assets", "fonts")

_WIDTH, _HEIGHT = 900, 600
_MARGIN = 50
_PAD_X = 48

_COLOR_PAGE_BG = "#eef1f4"
_COLOR_CARD_BG = "#ffffff"
_COLOR_SHADOW = (17, 24, 39, 40)
_COLOR_BRAND = "#16a34a"
_COLOR_TITLE = "#111827"
_COLOR_MUTED = "#6b7280"
_COLOR_DIVIDER = "#e5e7eb"

_TEXT = {
    "en": {
        "registration": "Registration Confirmed",
        "payment": "Payment Confirmed",
        "confirmed_on": "Confirmed {date}",
        "name_label": "Name",
        "package_label": "Package",
        "purchase_label": "Purchase",
        "footer": "Questions? Message Jack on Telegram.",
    },
    "my": {
        "registration": "Pendaftaran Disahkan",
        "payment": "Pembayaran Disahkan",
        "confirmed_on": "Disahkan {date}",
        "name_label": "Nama",
        "package_label": "Pakej",
        "purchase_label": "Pembelian",
        "footer": "Ada soalan? Mesej Jack di Telegram.",
    },
}


def _font(bold: bool, size: int) -> ImageFont.FreeTypeFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(_FONT_DIR, name), size)


def _text_width(draw: "ImageDraw.ImageDraw", text: str, font: ImageFont.FreeTypeFont) -> float:
    return draw.textlength(text, font=font)


def _fit_headline(draw: "ImageDraw.ImageDraw", text: str, max_width: float) -> ImageFont.FreeTypeFont:
    """Shrinks the headline font until it fits on one line, down to a floor size,
    then truncates with an ellipsis as a last resort (long product names)."""
    for size in (52, 46, 40, 34, 30):
        font = _font(bold=True, size=size)
        if _text_width(draw, text, font) <= max_width:
            return font, text
    font = _font(bold=True, size=30)
    while text and _text_width(draw, text + "…", font) > max_width:
        text = text[:-1]
    return font, (text + "…" if text else "…")


def generate_receipt_image(
    *, kind: str, region: str, name: str, label: str, when: datetime | None = None
) -> io.BytesIO:
    """Renders the receipt card as PNG bytes ready for Bot.send_photo.

    kind: "registration" or "payment" - picks the title and second row's label.
    region: "en" or "my" - picks the language.
    name: the client's name (or Telegram display name, for payments).
    label: the package tier name, or "{product} ({plan})" for payments.
    """
    strings = _TEXT.get(region, _TEXT["en"])
    when = when or datetime.now()

    img = Image.new("RGB", (_WIDTH, _HEIGHT), _COLOR_PAGE_BG)

    # Soft drop shadow behind the card.
    shadow = Image.new("RGBA", (_WIDTH, _HEIGHT), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        [_MARGIN, _MARGIN + 8, _WIDTH - _MARGIN, _HEIGHT - _MARGIN + 8],
        radius=24,
        fill=_COLOR_SHADOW,
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    page = Image.new("RGBA", img.size, _COLOR_PAGE_BG)
    img = Image.alpha_composite(page, shadow).convert("RGB")

    draw = ImageDraw.Draw(img)
    card_box = [_MARGIN, _MARGIN, _WIDTH - _MARGIN, _HEIGHT - _MARGIN]
    draw.rounded_rectangle(card_box, radius=24, fill=_COLOR_CARD_BG)

    content_left = _MARGIN + _PAD_X
    content_right = _WIDTH - _MARGIN - _PAD_X
    content_width = content_right - content_left

    y = _MARGIN + 42
    brand_font = _font(bold=True, size=18)
    draw.text((content_left, y), "EZYMAP ALGO", font=brand_font, fill=_COLOR_BRAND)
    y += 42

    title_font = _font(bold=True, size=32)
    title_text = strings["registration" if kind == "registration" else "payment"]
    draw.text((content_left, y), title_text, font=title_font, fill=_COLOR_TITLE)
    y += 46

    headline_font, headline_text = _fit_headline(draw, label, content_width)
    draw.text((content_left, y), headline_text, font=headline_font, fill=_COLOR_TITLE)
    y += headline_font.size + 22

    date_font = _font(bold=False, size=18)
    date_text = strings["confirmed_on"].format(date=when.strftime("%-d %b %Y"))
    draw.text((content_left, y), date_text, font=date_font, fill=_COLOR_MUTED)
    y += 44

    draw.line([(content_left, y), (content_right, y)], fill=_COLOR_DIVIDER, width=2)
    y += 34

    label_font = _font(bold=False, size=18)
    value_font = _font(bold=True, size=20)

    def draw_row(row_label: str, row_value: str, row_y: int) -> int:
        draw.text((content_left, row_y), row_label, font=label_font, fill=_COLOR_MUTED)
        value_width = _text_width(draw, row_value, value_font)
        draw.text((content_right - value_width, row_y - 1), row_value, font=value_font, fill=_COLOR_TITLE)
        return row_y + 40

    y = draw_row(strings["name_label"], name, y)
    package_label = strings["package_label"] if kind == "registration" else strings["purchase_label"]
    y = draw_row(package_label, label, y)

    y += 8
    draw.line([(content_left, y), (content_right, y)], fill=_COLOR_DIVIDER, width=2)
    y += 30

    footer_font = _font(bold=False, size=15)
    draw.text((content_left, y), strings["footer"], font=footer_font, fill=_COLOR_MUTED)

    buffer = io.BytesIO()
    buffer.name = "receipt.png"
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
