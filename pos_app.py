import tkinter as tk
from datetime import datetime
from functools import partial
from tkinter import messagebox

from PIL import Image, ImageTk

from product_catalog import ASSET_DIR, PRODUCTS_BY_CATEGORY


class PaymentDialog(tk.Toplevel):
    def __init__(
        self,
        master: tk.Tk,
        total_due: float,
        palette: dict[str, str],
        on_payment,
    ) -> None:
        super().__init__(master)
        self.total_due = total_due
        self.palette = palette
        self.on_payment = on_payment
        self.title("Payment")
        self.configure(bg=self.palette["bg"])
        self.geometry("460x380")
        self.minsize(460, 380)
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        card = tk.Frame(
            self,
            bg=self.palette["panel"],
            padx=20,
            pady=20,
            highlightthickness=2,
            highlightbackground=self.palette["cta"],
        )
        card.pack(expand=True, fill=tk.BOTH, padx=30, pady=25)
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(3, weight=1)

        header = tk.Frame(card, bg=self.palette["panel"])
        header.grid(row=0, column=0, sticky="ew")
        tk.Label(
            header,
            text="💳",
            font=("Segoe UI Emoji", 26),
            bg=self.palette["panel"],
        ).pack(side=tk.LEFT)
        tk.Label(
            header,
            text="Confirm Payment",
            font=("Montserrat", 18, "bold"),
            bg=self.palette["panel"],
            fg=self.palette["text_primary"],
        ).pack(anchor="w", padx=10)

        total_frame = tk.Frame(card, bg=self.palette["panel"], pady=5)
        total_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        tk.Label(
            total_frame,
            text="Total due today",
            font=("Montserrat", 11),
            bg=self.palette["panel"],
            fg=self.palette["text_muted"],
        ).pack(anchor="w")
        tk.Label(
            total_frame,
            text=f"₱{self.total_due:.2f}",
            font=("Montserrat", 20, "bold"),
            bg=self.palette["panel"],
            fg=self.palette["cta"],
        ).pack(anchor="w")

        form_frame = tk.Frame(card, bg=self.palette["panel"], pady=10)
        form_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))

        tk.Label(
            form_frame,
            text="Cash Tendered",
            font=("Montserrat", 11, "bold"),
            bg=self.palette["panel"],
            fg=self.palette["text_primary"],
        ).pack(anchor="w")

        self.cash_var = tk.StringVar()
        self.entry_border = tk.Frame(
            form_frame,
            bg=self.palette["bg"],
            highlightthickness=2,
            highlightbackground=self.palette["cta"],
            highlightcolor=self.palette["cta"],
        )
        self.entry_border.pack(fill=tk.X, pady=6)

        input_row = tk.Frame(self.entry_border, bg=self.palette["bg"])
        input_row.pack(fill=tk.X)

        prefix = tk.Label(
            input_row,
            text="₱",
            font=("Montserrat", 18, "bold"),
            bg=self.palette["bg"],
            fg=self.palette["cta"],
            width=2,
        )
        prefix.pack(side=tk.LEFT, padx=(10, 0), pady=6)

        self.entry = tk.Entry(
            input_row,
            textvariable=self.cash_var,
            font=("Montserrat", 18, "bold"),
            justify="right",
            bd=0,
            relief=tk.FLAT,
            bg="#fdf9f2",
            fg="#0b1726",
            insertbackground="#0b1726",
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(5, 12), pady=6)
        self.entry.focus_set()

        self.change_label = tk.Label(
            form_frame,
            text="Change: ₱0.00",
            font=("Montserrat", 11, "bold"),
            bg=self.palette["panel"],
            fg=self.palette["text_muted"],
        )
        self.change_label.pack(anchor="w", pady=(2, 4))

        self.error_label = tk.Label(
            form_frame,
            text="",
            font=("Montserrat", 10),
            bg=self.palette["panel"],
            fg="#ff8e8e",
        )
        self.error_label.pack(anchor="w", pady=(0, 4))

        tk.Frame(card, bg=self.palette["panel"], height=10).grid(row=3, column=0, sticky="nsew")

        button_frame = tk.Frame(card, bg=self.palette["panel"], pady=10)
        button_frame.grid(row=4, column=0, sticky="ew")

        confirm_btn = tk.Button(
            button_frame,
            text="CONFIRM PAYMENT",
            font=("Montserrat", 12, "bold"),
            bg=self.palette["cta"],
            fg="#1a1a1a",
            relief=tk.FLAT,
            command=self._confirm_payment,
            padx=12,
            pady=6,
        )
        confirm_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

        cancel_btn = tk.Button(
            button_frame,
            text="CANCEL",
            font=("Montserrat", 12, "bold"),
            bg=self.palette["button"],
            fg=self.palette["text_primary"],
            relief=tk.FLAT,
            command=self.destroy,
            padx=12,
            pady=6,
        )
        cancel_btn.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self._apply_hover(confirm_btn, self.palette["cta"], self.palette["button_hover"], cursor="hand2")
        self._apply_hover(cancel_btn, self.palette["button"], self.palette["button_active"], cursor="hand2")

        self.bind("<Return>", lambda _: self._confirm_payment())
        self.bind("<Escape>", lambda _: self.destroy())
        self.entry.bind("<KeyRelease>", self._preview_change)
        self.after(50, self._center_on_parent)

    def _confirm_payment(self) -> None:
        raw_value = self.cash_var.get().strip()
        try:
            amount = float(raw_value)
        except ValueError:
            self.error_label.config(text="Enter a valid number")
            return

        if amount < self.total_due:
            self.error_label.config(text="Cash is less than total")
            self.change_label.config(text="Change: ₱0.00", fg="#ff8e8e")
            return

        self.grab_release()
        self.destroy()
        self.on_payment(amount)

    def _preview_change(self, _: tk.Event) -> None:
        raw_value = self.cash_var.get().strip()
        try:
            amount = float(raw_value)
        except ValueError:
            self.change_label.config(text="Change: ₱0.00", fg=self.palette["text_muted"])
            self.error_label.config(text="")
            return

        change = amount - self.total_due
        fg = "#ff8e8e" if change < 0 else "#7fffd4"
        self.change_label.config(text=f"Change: ₱{max(change, 0):.2f}", fg=fg)
        self.error_label.config(text="" if change >= 0 else "Cash is less than total")

    def _apply_hover(self, widget: tk.Widget, normal_bg: str, hover_bg: str, *, cursor: str) -> None:
        def _enter(_: tk.Event) -> None:
            widget.configure(bg=hover_bg, cursor=cursor)

        def _leave(_: tk.Event) -> None:
            widget.configure(bg=normal_bg, cursor="arrow")

        widget.bind("<Enter>", _enter)
        widget.bind("<Leave>", _leave)

    def _center_on_parent(self) -> None:
        self.update_idletasks()
        master = self.master
        parent_x = master.winfo_rootx()
        parent_y = master.winfo_rooty()
        parent_w = master.winfo_width()
        parent_h = master.winfo_height()
        width = self.winfo_width()
        height = self.winfo_height()
        x = parent_x + (parent_w // 2) - (width // 2)
        y = parent_y + (parent_h // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{max(x, 0)}+{max(y, 0)}")


class ReceiptDialog(tk.Toplevel):
    def __init__(
        self,
        master: tk.Tk,
        palette: dict[str, str],
        items: list[dict],
        total: float,
        tendered: float,
        change: float,
    ) -> None:
        super().__init__(master)
        self.palette = palette
        self.title("Receipt")
        self.configure(bg=self.palette["bg"])
        self.geometry("420x520")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        card = tk.Frame(
            self,
            bg=self.palette["panel"],
            padx=20,
            pady=20,
            highlightthickness=2,
            highlightbackground=self.palette["accent"],
        )
        card.pack(expand=True, fill=tk.BOTH, padx=30, pady=25)

        header = tk.Frame(card, bg=self.palette["panel"], pady=5)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="🧾",
            font=("Segoe UI Emoji", 26),
            bg=self.palette["panel"],
        ).pack(side=tk.LEFT)
        tk.Label(
            header,
            text="KAPE SHOP RECEIPT",
            font=("Montserrat", 16, "bold"),
            bg=self.palette["panel"],
            fg=self.palette["text_primary"],
        ).pack(anchor="w", padx=8)

        tk.Label(
            card,
            text=datetime.now().strftime("%b %d, %Y • %I:%M %p"),
            font=("Montserrat", 10),
            bg=self.palette["panel"],
            fg=self.palette["text_muted"],
        ).pack(anchor="w", pady=(0, 10))

        list_wrapper = tk.Frame(card, bg=self.palette["panel"], pady=5)
        list_wrapper.pack(fill=tk.BOTH, expand=True)

        list_canvas = tk.Canvas(
            list_wrapper,
            bg=self.palette["panel"],
            highlightthickness=0,
            bd=0,
            height=220,
        )
        list_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scrollbar = tk.Scrollbar(list_wrapper, orient=tk.VERTICAL, command=list_canvas.yview)
        list_canvas.configure(yscrollcommand=list_scrollbar.set)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        list_frame = tk.Frame(list_canvas, bg=self.palette["panel"], padx=0, pady=0)
        list_canvas_window = list_canvas.create_window((0, 0), window=list_frame, anchor="nw")
        list_frame.bind(
            "<Configure>", lambda event: list_canvas.configure(scrollregion=list_canvas.bbox("all"))
        )
        list_canvas.bind(
            "<Configure>", lambda event: list_canvas.itemconfig(list_canvas_window, width=event.width)
        )
        list_canvas.bind("<MouseWheel>", lambda e: self._scroll_canvas(list_canvas, e))

        headings = tk.Frame(list_frame, bg=self.palette["panel"])
        headings.pack(fill=tk.X, pady=(0, 5))
        tk.Label(headings, text="Item", font=("Montserrat", 11, "bold"), bg=self.palette["panel"], fg=self.palette["text_primary"]).grid(row=0, column=0, sticky="w")
        tk.Label(headings, text="Qty", font=("Montserrat", 11, "bold"), bg=self.palette["panel"], fg=self.palette["text_primary"]).grid(row=0, column=1)
        tk.Label(headings, text="Subtotal", font=("Montserrat", 11, "bold"), bg=self.palette["panel"], fg=self.palette["text_primary"]).grid(row=0, column=2, sticky="e")
        headings.grid_columnconfigure(0, weight=2)
        headings.grid_columnconfigure(1, weight=1)
        headings.grid_columnconfigure(2, weight=1)

        rows_holder = tk.Frame(list_frame, bg=self.palette["panel_dark"], padx=10, pady=10)
        rows_holder.pack(fill=tk.BOTH, expand=True)

        for idx, item in enumerate(items):
            row = tk.Frame(rows_holder, bg=self.palette["panel_dark"])
            row.pack(fill=tk.X, pady=4)
            tk.Label(
                row,
                text=item["name"],
                font=("Montserrat", 11),
                bg=self.palette["panel_dark"],
                fg=self.palette["text_primary"],
            ).grid(row=0, column=0, sticky="w")
            tk.Label(
                row,
                text=f"x{item['qty']}",
                font=("Montserrat", 11, "bold"),
                bg=self.palette["panel_dark"],
                fg=self.palette["text_muted"],
            ).grid(row=0, column=1, padx=10)
            tk.Label(
                row,
                text=f"₱{item['subtotal']:.2f}",
                font=("Montserrat", 11),
                bg=self.palette["panel_dark"],
                fg=self.palette["text_primary"],
            ).grid(row=0, column=2, sticky="e")
            row.grid_columnconfigure(0, weight=2)
            row.grid_columnconfigure(1, weight=1)
            row.grid_columnconfigure(2, weight=1)

        summary = tk.Frame(card, bg=self.palette["panel"], pady=10)
        summary.pack(fill=tk.X)
        self._summary_line(summary, "Subtotal", total, bold=False)
        self._divider(summary)
        self._summary_line(summary, "TOTAL", total, bold=True, accent=True, font_size=14)
        self._summary_line(summary, "Cash", tendered, bold=False)
        self._summary_line(summary, "Change", change, bold=True)

        button_frame = tk.Frame(card, bg=self.palette["panel"], pady=5)
        button_frame.pack(fill=tk.X)
        close_btn = tk.Button(
            button_frame,
            text="CLOSE RECEIPT",
            font=("Montserrat", 12, "bold"),
            bg=self.palette["cta"],
            fg="#1a1a1a",
            relief=tk.FLAT,
            command=self._close,
            pady=6,
        )
        close_btn.pack(fill=tk.X)
        self._apply_hover(close_btn, self.palette["cta"], self.palette["button_hover"], cursor="hand2")

        self.bind("<Return>", lambda _: self._close())
        self.bind("<Escape>", lambda _: self._close())
        self.after(50, self._center_on_parent)

    def _summary_line(
        self,
        parent: tk.Frame,
        label: str,
        amount: float,
        *,
        bold: bool,
        accent: bool = False,
        font_size: int = 12,
    ) -> None:
        frame = tk.Frame(parent, bg=self.palette["panel"])
        frame.pack(fill=tk.X)
        tk.Label(
            frame,
            text=label,
            font=("Montserrat", font_size, "bold" if bold else "normal"),
            bg=self.palette["panel"],
            fg=self.palette["text_muted"],
        ).pack(side=tk.LEFT)
        tk.Label(
            frame,
            text=f"₱{amount:.2f}",
            font=("Montserrat", font_size + 1, "bold" if bold else "normal"),
            bg=self.palette["panel"],
            fg=self.palette["cta"] if accent else self.palette["text_primary"],
        ).pack(side=tk.RIGHT)

    def _divider(self, parent: tk.Frame) -> None:
        tk.Frame(parent, bg=self.palette["panel_dark"], height=2).pack(fill=tk.X, pady=6)

    def _scroll_canvas(self, canvas: tk.Canvas, event: tk.Event) -> None:
        delta = -1 * (event.delta // 120)
        if delta:
            canvas.yview_scroll(delta, "units")

    def _apply_hover(self, widget: tk.Widget, normal_bg: str, hover_bg: str, *, cursor: str) -> None:
        widget.bind("<Enter>", lambda _: widget.configure(bg=hover_bg, cursor=cursor))
        widget.bind("<Leave>", lambda _: widget.configure(bg=normal_bg, cursor="arrow"))

    def _center_on_parent(self) -> None:
        self.update_idletasks()
        master = self.master
        parent_x = master.winfo_rootx()
        parent_y = master.winfo_rooty()
        parent_w = master.winfo_width()
        parent_h = master.winfo_height()
        width = self.winfo_width()
        height = self.winfo_height()
        x = parent_x + (parent_w // 2) - (width // 2)
        y = parent_y + (parent_h // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{max(x, 0)}+{max(y, 0)}")

    def _close(self) -> None:
        self.grab_release()
        self.destroy()


class POSApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Kape POS")
        self.root.geometry("1200x700")
        self.root.configure(bg="#0b1726")
        self.root.minsize(1000, 600)

        self.palette = {
            "bg": "#0b1726",
            "panel": "#10243b",
            "panel_dark": "#0e1f33",
            "accent": "#1d4d7c",
            "button": "#173656",
            "button_active": "#1f5e95",
            "card_hover": "#1a3352",
            "button_hover": "#f7b866",
            "cta": "#f2a541",
            "text_primary": "#f5f6f7",
            "text_muted": "#9cb3c9",
        }

        self.products_by_category = PRODUCTS_BY_CATEGORY

        self.current_category = "Coffee"
        self.order = {}
        self.image_cache = {}

        self._build_layout()
        self._render_category_buttons()
        self._render_product_cards()
        self._render_order_items()

    def _build_layout(self) -> None:
        self.left_panel = tk.Frame(self.root, bg=self.palette["panel"], bd=0)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=25, pady=25)

        self.category_frame = tk.Frame(self.left_panel, bg=self.palette["panel"])
        self.category_frame.pack(fill=tk.X, pady=(0, 20))

        self.products_frame = tk.Frame(self.left_panel, bg=self.palette["panel"])
        self.products_frame.pack(fill=tk.BOTH, expand=True)

        self.order_panel = tk.Frame(
            self.root,
            bg=self.palette["panel_dark"],
            width=320,
            padx=20,
            pady=20,
        )
        self.order_panel.pack(side=tk.RIGHT, fill=tk.Y, pady=25, padx=(0, 25))

        order_title = tk.Label(
            self.order_panel,
            text="☕ ORDER",
            font=("Montserrat", 20, "bold"),
            bg=self.palette["panel_dark"],
            fg=self.palette["text_primary"],
        )
        order_title.pack(anchor="w", pady=(0, 10))

        self.order_list_wrapper = tk.Frame(self.order_panel, bg=self.palette["panel"], pady=0)
        self.order_list_wrapper.pack(fill=tk.BOTH, expand=True)

        self.order_canvas = tk.Canvas(
            self.order_list_wrapper,
            bg=self.palette["panel"],
            highlightthickness=0,
            bd=0,
        )
        self.order_canvas.pack(fill=tk.BOTH, expand=True)

        self.order_items_container = tk.Frame(
            self.order_canvas,
            bg=self.palette["panel"],
            pady=10,
            padx=10,
        )
        self.order_canvas_window = self.order_canvas.create_window((0, 0), window=self.order_items_container, anchor="nw")
        self.order_items_container.bind(
            "<Configure>",
            lambda event: self.order_canvas.configure(scrollregion=self.order_canvas.bbox("all")),
        )
        self.order_items_container.bind("<MouseWheel>", self._on_order_mousewheel)
        self.order_canvas.bind("<MouseWheel>", self._on_order_mousewheel)
        self.order_canvas.bind("<Enter>", lambda _: self._toggle_order_scroll(True))
        self.order_canvas.bind("<Leave>", lambda _: self._toggle_order_scroll(False))
        self.order_canvas.bind(
            "<Configure>",
            lambda event: self.order_canvas.itemconfig(self.order_canvas_window, width=event.width),
        )

        self.total_label = tk.Label(
            self.order_panel,
            text="TOTAL: 0",
            font=("Montserrat", 16, "bold"),
            bg=self.palette["panel_dark"],
            fg=self.palette["text_primary"],
        )
        self.total_label.pack(fill=tk.X, pady=(15, 10))

        self.checkout_button = tk.Button(
            self.order_panel,
            text="CHECKOUT",
            font=("Montserrat", 14, "bold"),
            bg=self.palette["cta"],
            fg="#1a1a1a",
            relief=tk.FLAT,
            command=self._checkout,
        )
        self.checkout_button.pack(fill=tk.X, ipady=10)
        self._apply_hover_style(
            self.checkout_button,
            normal_bg=self.palette["cta"],
            hover_bg=self.palette["button_hover"],
        )

    def _render_category_buttons(self) -> None:
        for widget in self.category_frame.winfo_children():
            widget.destroy()

        for idx, category in enumerate(self.products_by_category.keys()):
            is_active = category == self.current_category
            btn = tk.Button(
                self.category_frame,
                text=category.upper(),
                font=("Montserrat", 12, "bold"),
                bg=self.palette["button_active"] if is_active else self.palette["button"],
                fg=self.palette["text_primary"],
                activebackground=self.palette["button_active"],
                activeforeground=self.palette["text_primary"],
                relief=tk.FLAT,
                padx=20,
                pady=10,
                command=partial(self._switch_category, category),
            )
            btn.grid(row=0, column=idx, padx=(0 if idx == 0 else 10), sticky="ew")
            self.category_frame.grid_columnconfigure(idx, weight=1)
            if not is_active:
                self._apply_hover_style(
                    btn,
                    normal_bg=self.palette["button"],
                    hover_bg=self.palette["button_active"],
                )

    def _switch_category(self, category: str) -> None:
        if category == self.current_category:
            return
        self.current_category = category
        self._render_category_buttons()
        self._render_product_cards()

    def _render_product_cards(self) -> None:
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        products = self.products_by_category.get(self.current_category, [])
        columns = 3
        for idx, product in enumerate(products):
            card = tk.Frame(
                self.products_frame,
                bg=self.palette["panel_dark"],
                padx=10,
                pady=10,
                highlightthickness=2,
                highlightbackground=self.palette["panel"],
            )
            row = idx // columns
            col = idx % columns
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            img = self._get_cached_image(
                product["name"], product.get("image"), product["color"], size=(120, 120)
            )
            img_label = tk.Label(card, image=img, bg=self.palette["panel_dark"])
            img_label.image = img
            img_label.pack()

            name_label = tk.Label(
                card,
                text=product["name"],
                font=("Montserrat", 12, "bold"),
                bg=self.palette["panel_dark"],
                fg=self.palette["text_primary"],
            )
            name_label.pack(pady=(10, 0))

            price_label = tk.Label(
                card,
                text=f"₱{product['price']:.2f}",
                font=("Montserrat", 11),
                bg=self.palette["panel_dark"],
                fg=self.palette["text_muted"],
            )
            price_label.pack(pady=(0, 10))

            add_btn = tk.Button(
                card,
                text="ADD",
                font=("Montserrat", 11, "bold"),
                bg=self.palette["cta"],
                fg="#1a1a1a",
                relief=tk.FLAT,
                command=partial(self._add_to_order, product),
            )
            add_btn.pack(fill=tk.X)

            self._apply_hover_style(
                card,
                normal_bg=self.palette["panel_dark"],
                hover_bg=self.palette["card_hover"],
                extra_widgets=[img_label, name_label, price_label],
                highlight_widget=card,
                normal_border=self.palette["panel"],
                hover_border=self.palette["cta"],
            )
            self._apply_hover_style(
                add_btn,
                normal_bg=self.palette["cta"],
                hover_bg=self.palette["button_hover"],
            )

        for i in range(columns):
            self.products_frame.grid_columnconfigure(i, weight=1)

    def _on_order_mousewheel(self, event: tk.Event) -> None:
        if hasattr(self, "order_canvas"):
            delta = -1 * (event.delta // 120)
            if delta != 0:
                self.order_canvas.yview_scroll(delta, "units")

    def _toggle_order_scroll(self, bind: bool) -> None:
        if bind:
            self.order_canvas.bind_all("<MouseWheel>", self._on_order_mousewheel)
        else:
            self.order_canvas.unbind_all("<MouseWheel>")

    def _apply_hover_style(
        self,
        widget: tk.Widget,
        *,
        normal_bg: str,
        hover_bg: str,
        normal_fg: str | None = None,
        hover_fg: str | None = None,
        extra_widgets: list[tk.Widget] | None = None,
        cursor: str = "hand2",
        highlight_widget: tk.Widget | None = None,
        normal_border: str | None = None,
        hover_border: str | None = None,
    ) -> None:
        extra_widgets = extra_widgets or []

        def _set_colors(bg: str, fg: str | None, border: str | None) -> None:
            try:
                widget.configure(bg=bg)
                if fg is not None:
                    widget.configure(fg=fg)
            except tk.TclError:
                pass
            for child in extra_widgets:
                try:
                    child.configure(bg=bg)
                except tk.TclError:
                    continue
            if highlight_widget is not None and border is not None:
                try:
                    highlight_widget.configure(highlightbackground=border, highlightcolor=border)
                except tk.TclError:
                    pass

        def _on_enter(_: tk.Event) -> None:
            widget.configure(cursor=cursor)
            _set_colors(hover_bg, hover_fg, hover_border)

        def _on_leave(_: tk.Event) -> None:
            widget.configure(cursor="arrow")
            _set_colors(normal_bg, normal_fg, normal_border)

        widget.bind("<Enter>", _on_enter)
        widget.bind("<Leave>", _on_leave)

    def _get_cached_image(
        self, key: str, image_name: str | None, color: str, size: tuple[int, int]
    ) -> tk.PhotoImage:
        cache_key = f"{key}:{size[0]}x{size[1]}"
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        img = self._load_image(image_name, color, size)
        self.image_cache[cache_key] = img
        return img

    def _load_image(self, image_name: str | None, color: str, size: tuple[int, int]) -> tk.PhotoImage:
        path = ASSET_DIR / image_name if image_name else None
        resample_filter = getattr(Image, "Resampling", Image).LANCZOS
        if path and path.exists():
            try:
                pil_img = Image.open(path).convert("RGBA")
                pil_img = pil_img.resize(size, resample=resample_filter)
            except Exception:
                pil_img = Image.new("RGB", size, color)
        else:
            pil_img = Image.new("RGB", size, color)
        return ImageTk.PhotoImage(pil_img)

    def _add_to_order(self, product: dict) -> None:
        name = product["name"]
        item = self.order.get(name)
        if item is None:
            item = {
                "qty": 1,
                "price": product["price"],
                "color": product["color"],
                "image": product.get("image"),
            }
        else:
            item["qty"] += 1
        self.order[name] = item
        self._render_order_items()

    def _update_qty(self, name: str, delta: int) -> None:
        if name not in self.order:
            return
        self.order[name]["qty"] += delta
        if self.order[name]["qty"] <= 0:
            del self.order[name]
        self._render_order_items()

    def _render_order_items(self) -> None:
        scroll_pos = None
        if hasattr(self, "order_canvas"):
            try:
                scroll_pos = self.order_canvas.yview()
            except tk.TclError:
                scroll_pos = None

        for widget in self.order_items_container.winfo_children():
            widget.destroy()

        if not self.order:
            empty_label = tk.Label(
                self.order_items_container,
                text="No items yet",
                font=("Montserrat", 12),
                bg=self.palette["panel"],
                fg=self.palette["text_muted"],
            )
            empty_label.pack(expand=True)
        else:
            for name, info in self.order.items():
                row_shell = tk.Frame(self.order_items_container, bg=self.palette["panel"], pady=2)
                row_shell.pack(fill=tk.X, pady=4)

                row_frame = tk.Frame(
                    row_shell,
                    bg=self.palette["panel_dark"],
                    padx=10,
                    pady=8,
                    highlightthickness=1,
                    highlightbackground=self.palette["card_hover"],
                )
                row_frame.pack(fill=tk.X)

                img = self._get_cached_image(name, info.get("image"), info["color"], size=(60, 60))
                thumb = tk.Label(row_frame, image=img, bg=self.palette["panel_dark"])
                thumb.image = img
                thumb.configure(width=60, height=60)
                thumb.pack(side=tk.LEFT)

                detail_frame = tk.Frame(row_frame, bg=self.palette["panel_dark"])
                detail_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)

                name_label = tk.Label(
                    detail_frame,
                    text=name,
                    font=("Montserrat", 12, "bold"),
                    bg=self.palette["panel_dark"],
                    fg=self.palette["text_primary"],
                )
                name_label.pack(anchor="w")

                price_label = tk.Label(
                    detail_frame,
                    text=f"₱{info['price']:.2f}",
                    font=("Montserrat", 11),
                    bg=self.palette["panel_dark"],
                    fg=self.palette["text_muted"],
                )
                price_label.pack(anchor="w")

                qty_frame = tk.Frame(row_frame, bg=self.palette["panel_dark"])
                qty_frame.pack(side=tk.RIGHT)

                minus_btn = tk.Button(
                    qty_frame,
                    text="-",
                    font=("Montserrat", 12, "bold"),
                    width=2,
                    bg=self.palette["button"],
                    fg=self.palette["text_primary"],
                    relief=tk.FLAT,
                    command=partial(self._update_qty, name, -1),
                )
                minus_btn.pack(side=tk.LEFT, padx=2)
                self._apply_hover_style(
                    minus_btn,
                    normal_bg=self.palette["button"],
                    hover_bg=self.palette["button_active"],
                )

                qty_label = tk.Label(
                    qty_frame,
                    text=str(info["qty"]),
                    font=("Montserrat", 12, "bold"),
                    width=3,
                    bg=self.palette["panel_dark"],
                    fg=self.palette["text_primary"],
                )
                qty_label.pack(side=tk.LEFT)

                plus_btn = tk.Button(
                    qty_frame,
                    text="+",
                    font=("Montserrat", 12, "bold"),
                    width=2,
                    bg=self.palette["button_active"],
                    fg=self.palette["text_primary"],
                    relief=tk.FLAT,
                    command=partial(self._update_qty, name, 1),
                )
                plus_btn.pack(side=tk.LEFT, padx=2)
                self._apply_hover_style(
                    plus_btn,
                    normal_bg=self.palette["button_active"],
                    hover_bg=self.palette["accent"],
                )

        self._update_total()
        if scroll_pos:
            self.order_canvas.yview_moveto(scroll_pos[0])

    def _update_total(self) -> None:
        total = sum(info["price"] * info["qty"] for info in self.order.values())
        self.total_label.config(text=f"TOTAL: ₱{total:.2f}")

    def _checkout(self) -> None:
        if not self.order:
            messagebox.showinfo("Checkout", "Please add an item to proceed.")
            return
        total = sum(info["price"] * info["qty"] for info in self.order.values())
        PaymentDialog(self.root, total, self.palette, self._finalize_checkout)

    def _finalize_checkout(self, amount_tendered: float) -> None:
        if not self.order:
            return
        order_snapshot = [
            {
                "name": name,
                "qty": info["qty"],
                "price": info["price"],
                "subtotal": info["price"] * info["qty"],
            }
            for name, info in self.order.items()
        ]
        total = sum(item["subtotal"] for item in order_snapshot)
        change = amount_tendered - total
        ReceiptDialog(
            self.root,
            self.palette,
            order_snapshot,
            total,
            amount_tendered,
            change,
        )
        self.order.clear()
        self._render_order_items()


def main() -> None:
    root = tk.Tk()
    POSApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
