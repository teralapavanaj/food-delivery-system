# FoodFlow — UI Mock-up

A polished, dark-themed front-end for the Food Delivery Management
System — built to **show**, not to run as the real backend. It mirrors
the Python logic in `../models.py` / `../main.py` (restaurants, food
items with live stock, polymorphic delivery pricing, order status
tracking) entirely in client-side JavaScript, so it opens instantly
with nothing to install.

## How to open it

**Easiest:** double-click `index.html` — it opens directly in your
browser (Chrome, Edge, Firefox).

**From VS Code:** right-click `index.html` → "Open with Live Server"
(if you have that extension), or just double-click it in your file
explorer. No Python, no server, no build step needed.

## What to show your instructor

1. **Restaurants** — browse partner restaurants as cards (rating, cuisine).
2. **Search Menu** — filter by name / category / restaurant; stock
   pills show "in stock", "low stock", or "out of stock" / "unavailable"
   live, matching the `available` flag + `stock` count from the Python
   model.
3. **Cart & Checkout** — add items, switch delivery type (Standard /
   Express / Scheduled) and watch the charge recalculate instantly —
   this is the polymorphic `calculate_charge()` behaviour from
   `models.py`, reproduced in the UI.
4. **Track Orders** — place an order, then advance it through
   `PLACED → CONFIRMED → OUT_FOR_DELIVERY → DELIVERED` with a visual
   progress tracker, or cancel it early.
5. **Customer** — profile card + order history.

Try adding more Gulab Jamun (`F3`) than the 2 left in stock — you'll
get the same "insufficient stock" rejection the Python CLI gives, as
a toast notification instead of console text.

## Note

This is a visual demo only — state resets on page reload (no backend,
no database). The actual persistent logic (CSV/JSON, real exception
classes) lives in the Python files one level up; this UI is the
"what it could look like" layer for a presentation.
