"""
Handles all CSV/JSON persistence for the system:
- restaurants.csv
- food_items.csv
- customers.json
- orders.json  (written as orders are placed)

All file operations are wrapped so a missing/corrupt file raises a
FileOperationError instead of crashing the program, and bad rows are
skipped with a warning rather than aborting the whole load.
"""

import csv
import json
import os

from exceptions import FileOperationError, InvalidOrderIDError, InvalidStatusTransitionError
from models import FoodItem, Restaurant, Customer, Order


class DataManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.restaurants = {}   # restaurant_id -> Restaurant
        self.food_items = {}    # food_id -> FoodItem
        self.customers = {}     # customer_id -> Customer

    def _path(self, filename):
        return os.path.join(self.data_dir, filename)

    # ------------------------------------------------------------
    # Restaurants (CSV)
    # ------------------------------------------------------------
    def load_restaurants(self, filename="restaurants.csv"):
        path = self._path(filename)
        if not os.path.exists(path):
            raise FileOperationError(filename, "file not found")
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        r = Restaurant(
                            row["restaurant_id"], row["name"], row["cuisine"], row.get("rating", 0)
                        )
                        self.restaurants[r.restaurant_id] = r
                    except (KeyError, ValueError) as e:
                        print(f"  [skip] bad restaurant row {row}: {e}")
        except (OSError, csv.Error) as e:
            raise FileOperationError(filename, str(e))

    # ------------------------------------------------------------
    # Food items (CSV)
    # ------------------------------------------------------------
    def load_food_items(self, filename="food_items.csv"):
        path = self._path(filename)
        if not os.path.exists(path):
            raise FileOperationError(filename, "file not found")
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        item = FoodItem(
                            row["food_id"],
                            row["name"],
                            row["category"],
                            row["price"],
                            row["restaurant_id"],
                            row.get("available", "true"),
                            row.get("stock", 0),
                        )
                        self.food_items[item.food_id] = item
                        restaurant = self.restaurants.get(item.restaurant_id)
                        if restaurant:
                            restaurant.add_food_item(item)
                    except (KeyError, ValueError) as e:
                        print(f"  [skip] bad food item row {row}: {e}")
        except (OSError, csv.Error) as e:
            raise FileOperationError(filename, str(e))

    def save_food_items(self, filename="food_items.csv"):
        """Persist current stock/availability back to the CSV (call after each order)."""
        path = self._path(filename)
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["food_id", "name", "category", "price", "restaurant_id", "available", "stock"]
                )
                writer.writeheader()
                for item in self.food_items.values():
                    writer.writerow(item.to_dict())
        except OSError as e:
            raise FileOperationError(filename, str(e))

    # ------------------------------------------------------------
    # Customers (JSON)
    # ------------------------------------------------------------
    def load_customers(self, filename="customers.json"):
        path = self._path(filename)
        if not os.path.exists(path):
            # Not fatal: a fresh system may have zero customers yet.
            return
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            for row in data:
                c = Customer(row["customer_id"], row["name"], row["phone"], row["address"])
                c.order_history = row.get("order_history", [])
                self.customers[c.customer_id] = c
        except (OSError, json.JSONDecodeError, KeyError) as e:
            raise FileOperationError(filename, str(e))

    def save_customers(self, filename="customers.json"):
        path = self._path(filename)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump([c.to_dict() for c in self.customers.values()], f, indent=2)
        except OSError as e:
            raise FileOperationError(filename, str(e))

    # ------------------------------------------------------------
    # Orders (JSON) - append-only order log
    # ------------------------------------------------------------
    def save_order(self, order, filename="orders.json"):
        path = self._path(filename)
        orders = []
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as f:
                    orders = json.load(f)
            except (OSError, json.JSONDecodeError):
                orders = []
        orders.append(order.to_dict())
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(orders, f, indent=2)
        except OSError as e:
            raise FileOperationError(filename, str(e))

    def _load_orders_raw(self, filename="orders.json"):
        path = self._path(filename)
        if not os.path.exists(path):
            return []
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            raise FileOperationError(filename, str(e))

    def get_order_status(self, order_id, filename="orders.json"):
        for record in self._load_orders_raw(filename):
            if record["order_id"] == str(order_id):
                return record
        raise InvalidOrderIDError(order_id)

    def update_order_status(self, order_id, new_status=None, filename="orders.json"):
        """
        Move an order to the next stage in Order.STATUS_FLOW (default), or to a
        specific `new_status` if given. Returns the updated order record.
        Raises InvalidOrderIDError / InvalidStatusTransitionError as appropriate.
        """
        orders = self._load_orders_raw(filename)
        record = None
        for r in orders:
            if r["order_id"] == str(order_id):
                record = r
                break
        if record is None:
            raise InvalidOrderIDError(order_id)

        current = record["status"]
        if new_status is None:
            if current == "CANCELLED":
                raise InvalidStatusTransitionError(current, "advance")
            idx = Order.STATUS_FLOW.index(current)
            if idx == len(Order.STATUS_FLOW) - 1:
                raise InvalidStatusTransitionError(current, "further")
            record["status"] = Order.STATUS_FLOW[idx + 1]
        elif new_status == "CANCELLED":
            if current in ("OUT_FOR_DELIVERY", "DELIVERED", "CANCELLED"):
                raise InvalidStatusTransitionError(current, "CANCELLED")
            record["status"] = "CANCELLED"
        else:
            raise InvalidStatusTransitionError(current, new_status)

        try:
            with open(self._path(filename), "w", encoding="utf-8") as f:
                json.dump(orders, f, indent=2)
        except OSError as e:
            raise FileOperationError(filename, str(e))
        return record

    # ------------------------------------------------------------
    # Load everything at startup
    # ------------------------------------------------------------
    def load_all(self):
        self.load_restaurants()
        self.load_food_items()
        self.load_customers()
