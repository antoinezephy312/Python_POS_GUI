from pathlib import Path

ASSET_DIR = Path(__file__).parent / "assets"

PRODUCTS_BY_CATEGORY = {
    "Coffee": [
        {"name": "Kape Brew", "price": 100, "color": "#28507a", "image": "kape_brew.png"},
        {"name": "Latte", "price": 120, "color": "#2e618f", "image": "latte.png"},
        {"name": "Mocha", "price": 150, "color": "#325b82", "image": "mocha.png"},
        {"name": "Americano", "price": 110, "color": "#274465", "image": "americano.png"},
        {"name": "Flat White", "price": 135, "color": "#2b4d70", "image": "flat_white.png"},
        {"name": "Espresso", "price": 90, "color": "#244059", "image": "espresso.png"},
    ],
    "Pastry": [
        {"name": "Croissant", "price": 80, "color": "#7c4b2f", "image": "croissant.png"},
        {"name": "Bagel", "price": 70, "color": "#925b38", "image": "bagel.png"},
        {"name": "Banana Bread", "price": 95, "color": "#8b5131", "image": "banana_bread.png"},
        {"name": "Donut", "price": 65, "color": "#aa6d40", "image": "donut.png"},
    ],
    "Iced Coffee": [
        {"name": "Iced Latte", "price": 130, "color": "#2a597e", "image": "iced_latte.png"},
        {"name": "Cold Brew", "price": 140, "color": "#1e4564", "image": "cold_brew.png"},
        {"name": "Iced Mocha", "price": 150, "color": "#244f73", "image": "iced_mocha.png"},
        {"name": "Spanish Latte", "price": 160, "color": "#30577c", "image": "spanish_latte.png"},
    ],
}
