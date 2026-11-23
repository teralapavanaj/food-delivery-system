"""
Non-interactive smoke test / demo of the core system, exercising:
 - loading CSV/JSON data
 - exception handling (bad food ID, unavailable item, bad quantity,
   insufficient stock, bad order ID, invalid status transition)
 - polymorphism across delivery types
 - placing orders, stock being deducted and persisted
 - tracking / advancing an order's delivery status

Run:  python demo.py
"""

from data_manager import DataManager
from models import Order, StandardDelivery, ExpressDelivery, ScheduledDelivery
from exceptions import (
    InvalidFoodIDError,
    ItemUnavailableError,
    InvalidQuantityError,
    InsufficientStockError,
    InvalidOrderIDError,
    InvalidStatusTransitionError,
)


def main():
    dm = DataManager(data_dir="data")
    dm.load_all()
    print(f"Loaded {len(dm.restaurants)} restaurants, {len(dm.food_items)} food items, "
          f"{len(dm.customers)} customers.\n")

    customer = dm.customers["C1"]
    restaurant = dm.restaurants["R1"]

    print("--- Current stock at Spice Villa ---")
    for item in restaurant.menu:
        print(" ", item)

    print("\n--- Placing a valid order (Standard delivery) ---")
    order = Order(customer, restaurant, StandardDelivery())
    order.add_line(dm.food_items["F1"], 2)   # Paneer Butter Masala x2
    order.add_line(dm.food_items["F2"], 1)   # Masala Dosa x1
    print(order.receipt())
    customer.order_history.append(order.order_id)
    dm.save_order(order)
    dm.save_customers()
    dm.save_food_items()  # persists the stock deduction back to food_items.csv

    print("\n--- Stock after that order (F1 and F2 both reduced) ---")
    for item in restaurant.menu:
        print(" ", item)

    print("\n--- Same-style cart, Express delivery (polymorphism: different charge) ---")
    order2 = Order(customer, restaurant, ExpressDelivery())
    order2.add_line(dm.food_items["F6"], 1)  # Chicken Biryani x1
    print(order2.receipt())

    print("\n--- Exception handling checks ---")
    try:
        if "DOES_NOT_EXIST" not in dm.food_items:
            raise InvalidFoodIDError("DOES_NOT_EXIST")
    except InvalidFoodIDError as e:
        print(f"Caught expected error: {e}")

    try:
        order.add_line(dm.food_items["F21"], 1)  # Spring Rolls (Dragon Wok), available=false
    except ItemUnavailableError as e:
        print(f"Caught expected error: {e}")

    try:
        order.add_line(dm.food_items["F1"], -3)
    except InvalidQuantityError as e:
        print(f"Caught expected error: {e}")

    try:
        # F3 (Gulab Jamun) starts with only 2 in stock -- ask for way more.
        order.add_line(dm.food_items["F3"], 999)
    except InsufficientStockError as e:
        print(f"Caught expected error: {e}")

    try:
        dm.get_order_status("NOT_A_REAL_ORDER")
    except InvalidOrderIDError as e:
        print(f"Caught expected error: {e}")

    print("\n--- Order status tracking ---")
    record = dm.get_order_status(order.order_id)
    print(f"Order #{order.order_id} status: {record['status']}")

    record = dm.update_order_status(order.order_id)  # PLACED -> CONFIRMED
    print(f"Advanced to: {record['status']}")
    record = dm.update_order_status(order.order_id)  # CONFIRMED -> OUT_FOR_DELIVERY
    print(f"Advanced to: {record['status']}")
    record = dm.update_order_status(order.order_id)  # OUT_FOR_DELIVERY -> DELIVERED
    print(f"Advanced to: {record['status']}")

    try:
        dm.update_order_status(order.order_id)  # already DELIVERED, can't go further
    except InvalidStatusTransitionError as e:
        print(f"Caught expected error: {e}")

    print("\nDemo complete. Orders + statuses in data/orders.json, "
          "stock changes saved to data/food_items.csv, "
          "customers in data/customers.json.")


if __name__ == "__main__":
    main()
