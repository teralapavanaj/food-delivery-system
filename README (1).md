# Food Delivery Management System (Prototype)

A console-based Food Delivery Management System in Python, covering:

- **Entities**: `FoodItem`, `Restaurant`, `Customer`
- **Inheritance & polymorphism**: `DeliveryType` (abstract) with
  `StandardDelivery`, `ExpressDelivery`, `ScheduledDelivery` subclasses,
  each overriding `calculate_charge()` and `estimated_time_minutes()`
- **Search**: by name, category, or restaurant
- **Stock tracking**: each `FoodItem` has a `stock` count (not just an
  available/unavailable flag). Placing an order deducts stock
  immediately; ordering more than what's left raises
  `InsufficientStockError` and the stock is left untouched
- **Order status tracking**: every order moves through
  `PLACED -> CONFIRMED -> OUT_FOR_DELIVERY -> DELIVERED` (or
  `CANCELLED` from `PLACED`/`CONFIRMED`). Look up or advance an
  order's status any time via menu option 7 or `DataManager.get_order_status()`
  / `update_order_status()`
- **Persistence**: restaurants + food items (with stock) from CSV,
  customers + orders (with status) as JSON
- **Exception handling**: custom exceptions for invalid IDs,
  unavailable items, bad quantities, insufficient stock, invalid
  order IDs, invalid status transitions, and file I/O failures —
  all share a `FoodDeliveryError` base so the CLI catches them in
  one place and keeps running

## Files

```
food_delivery_system/
├── main.py           # Interactive CLI (menu-driven)
├── demo.py           # Non-interactive scripted demo (run this first)
├── models.py         # FoodItem, Restaurant, Customer, Order, DeliveryType hierarchy
├── data_manager.py   # CSV/JSON load & save, wrapped error handling
├── exceptions.py      # Custom exception classes
├── data/
│   ├── restaurants.csv
│   ├── food_items.csv
│   ├── customers.json
│   └── orders.json    # created automatically when an order is placed
└── README.md
```

## Setup in VS Code

1. Install Python 3.9+ (no external packages needed — standard library only).
2. Open the `food_delivery_system` folder in VS Code (`File > Open Folder`).
3. Open a terminal in VS Code (`` Ctrl+` ``).

## Run

Scripted demo (no typing required, shows everything working):
```
python demo.py
```

Full interactive menu:
```
python main.py
```

Sample menu flow for `main.py`:
1. Option `1` — list restaurants (`R1`...`R10`)
2. Option `3` — view a restaurant's menu, including live stock (enter `R1`)
3. Option `5` — place an order. Enter a customer ID — `C1` is pre-seeded,
   or type any new ID and it registers you on the spot (name, phone,
   address). Pick a restaurant and delivery type, then you're asked
   **who to deliver to** (recipient name, phone, address) — press
   Enter on each to keep your saved details, or type new ones to send
   the order elsewhere/to someone else. Then add food IDs + quantities,
   blank line to finish. Note the order ID printed at the end.
4. Option `7` — check that order's status, press `n` to advance it
   one stage (`PLACED -> CONFIRMED -> OUT_FOR_DELIVERY -> DELIVERED`),
   or `c` to cancel it (only while `PLACED`/`CONFIRMED`)
5. Option `6` — view that customer's order history

### How each error case is handled

| Situation | What happens |
|---|---|
| Food ID doesn't exist / belongs to another restaurant | `InvalidFoodIDError` — rejected, cart untouched |
| Item's `available` flag is off | `ItemUnavailableError` — rejected |
| Quantity isn't a positive integer | `InvalidQuantityError` — rejected |
| Quantity exceeds remaining `stock` | `InsufficientStockError` — rejected, stock **not** deducted |
| Order ID not found when tracking | `InvalidOrderIDError` |
| Trying to advance past `DELIVERED`, or cancel after `OUT_FOR_DELIVERY` | `InvalidStatusTransitionError` |
| A data file is missing/corrupt | `FileOperationError` — reported, program doesn't crash |

Every one of these is caught by `main.py`'s single `except FoodDeliveryError`
handler (they all inherit from it), printed as `Error: ...`, and the menu
loop continues — nothing crashes the program.

## Extending it

- Add more restaurants/food items by appending rows to the CSV files
  (same columns).
- Add a new delivery strategy by subclassing `DeliveryType` in
  `models.py` and registering it in `DELIVERY_TYPES`.
- Swap the CLI for a GUI/web frontend later without touching
  `models.py` or `data_manager.py` — they have no I/O-to-console coupling.
