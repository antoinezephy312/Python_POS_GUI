# ☕ Kape POS (Tkinter)

> Modern-looking point-of-sale UI prototype recreated with Tkinter and Pillow.

![Status](https://img.shields.io/badge/status-polished-blue)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776ab?logo=python&logoColor=white)
![License](https://img.shields.io/badge/use-at_your_own_risk-orange)

### ✨ Highlights
- **Pixel-perfect layout** matching the original Figma reference: category tabs, product cards with photos, and a navy/orange palette.
- **Interactive order drawer** with quantity steppers, running totals, and validation before checkout.
- **Stylish payment modal** centered on screen, showing cash entry, live change preview, and inline warnings.
- **Branded receipt dialog** that lists every line item with cash/change summary and a close button.
- **Placeholder asset pipeline** via `generate_product_assets.py` so you can refresh all thumbnails instantly.

### 🧰 Requirements
- Python 3.11+
- [Pillow](https://pypi.org/project/Pillow/)

### 🚀 Quick Start
```powershell
# optional: activate your virtual environment
pip install pillow
python generate_product_assets.py   # only if you need to regenerate placeholders
python pos_app.py
```
Add items from the grid, review them in the order panel, click **CHECKOUT**, enter payment, and admire the receipt pop-up.

### 🎨 Customize It
- **Product catalog** → tweak `product_catalog.py` for names, prices, palette hints, and image filenames.
- **Images** → drop new PNG/JPG assets in `assets/` (reuse filenames or update the catalog).
- **Branding** → play with `POSApp.palette` to reskin buttons, cards, and backgrounds.
- **Placeholder refresh** → run `python generate_product_assets.py` whenever you add products and need quick mock art.

### 🗂️ Project Layout
```
Python_POS_KYLE/
├─ assets/                 # product thumbnails
├─ generate_product_assets.py
├─ pos_app.py              # main Tkinter application
└─ product_catalog.py      # central product data
```

### 🧭 Roadmap Ideas
1. Persist sales history to CSV/SQLite
2. Export printable/PDF receipts
3. Add discounts, loyalty points, or keyboard shortcuts

---
**Author:** syntaxt0x1c

Feel free to fork, restyle, and publish—just have fun brewing your own POS flavor! 🎉
