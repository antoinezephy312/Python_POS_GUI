from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from product_catalog import ASSET_DIR, PRODUCTS_BY_CATEGORY


def _wrap_text(text: str, max_width: int, draw: ImageDraw.ImageDraw, font: ImageFont.ImageFont) -> str:
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if draw.textlength(test_line, font=font) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return "\n".join(lines)


def _create_placeholder(product: dict, font: ImageFont.ImageFont) -> None:
    size = (180, 180)
    canvas = Image.new("RGB", size, product["color"])
    draw = ImageDraw.Draw(canvas)
    wrapped = _wrap_text(product["name"], size[0] - 20, draw, font)
    draw.multiline_text(
        (size[0] // 2, size[1] // 2),
        wrapped,
        fill="#f9f6eb",
        font=font,
        anchor="mm",
        align="center",
        spacing=4,
    )
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    path = ASSET_DIR / product["image"]
    canvas.save(path, format="PNG")


def main() -> None:
    font = ImageFont.load_default()
    for category in PRODUCTS_BY_CATEGORY.values():
        for product in category:
            _create_placeholder(product, font)


if __name__ == "__main__":
    main()
