"""
Core domain classes for the Food Delivery Management System.

Class design (matches the project spec):
- FoodItem, Restaurant, Customer -> core entities
- Order -> ties a customer, restaurant, and food items together
- DeliveryType (abstract base) -> StandardDelivery / ExpressDelivery /
  ScheduledDelivery subclasses demonstrate INHERITANCE and POLYMORPHISM
  through an overridden calculate_charge() method.
"""

from abc import ABC, abstractmethod
from datetime import datetime

from exceptions import (
    InvalidQuantityError,
    ItemUnavailableError,
    InsufficientStockError,
    InvalidStatusTransitionError,
)


class FoodItem:
    """A single menu item offered by a restaurant.

    `available` is a manual on/off switch a restaurant can flip (e.g. the
    kitchen stopped making it today). `stock` is the actual unit count
    left — it goes down as orders are placed and is the thing that runs
    out on its own, independent of the `available` flag.
    """

    def __init__(self, food_id, name, category, price, restaurant_id, available=True, stock=0):
        self.food_id = str(food_id)
        self.name = name
        self.category = category
        self.price = float(price)
        self.restaurant_id = str(restaurant_id)
        self.available = self._parse_bool(available)
        self.stock = int(stock)

    @staticmethod
    def _parse_bool(value):
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in ("1", "true", "yes", "y")

    def reduce_stock(self, quantity):
        """Deduct `quantity` units. Raises InsufficientStockError if not enough left."""
        if quantity > self.stock:
            raise InsufficientStockError(self.name, quantity, self.stock)
        self.stock -= quantity

    def restock(self, quantity):
        """Add units back (e.g. a restaurant topping up supply)."""
        if quantity < 0:
            raise InvalidQuantityError(quantity)
        self.stock += quantity

    def to_dict(self):
        return {
            "food_id": self.food_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "restaurant_id": self.restaurant_id,
            "available": self.available,
            "stock": self.stock,
        }

    def __str__(self):
        if not self.available:
            status = "Unavailable"
        elif self.stock <= 0:
            status = "Out of stock"
        else:
            status = f"{self.stock} left"
        return f"[{self.food_id}] {self.name} ({self.category}) - Rs.{self.price:.2f} - {status}"


class Restaurant:
    """A restaurant that owns a set of food items."""

    def __init__(self, restaurant_id, name, cuisine, rating=0.0):
        self.restaurant_id = str(restaurant_id)
        self.name = name
        self.cuisine = cuisine
        self.rating = float(rating)
        self.menu = []  # list of FoodItem, populated by DataManager

    def add_food_item(self, food_item):
        self.menu.append(food_item)

    def to_dict(self):
        return {
            "restaurant_id": self.restaurant_id,
            "name": self.name,
            "cuisine": self.cuisine,
            "rating": self.rating,
        }

    def __str__(self):
        return f"[{self.restaurant_id}] {self.name} ({self.cuisine}) - {self.rating}/5"


class Customer:
    """A registered customer who places orders."""

    def __init__(self, customer_id, name, phone, address):
        self.customer_id = str(customer_id)
        self.name = name
        self.phone = phone
        self.address = address
        self.order_history = []  # list of Order IDs

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "phone": self.phone,
            "address": self.address,
            "order_history": self.order_history,
        }

    def __str__(self):
        return f"[{self.customer_id}] {self.name} - {self.phone} - {self.address}"


# ---------------------------------------------------------------------
# Delivery types: INHERITANCE + POLYMORPHISM
# ---------------------------------------------------------------------

class DeliveryType(ABC):
    """Abstract base for all delivery strategies."""

    name = "Generic"

    @abstractmethod
    def calculate_charge(self, order_subtotal):
        """Return the delivery charge for a given order subtotal."""
        raise NotImplementedError

    def estimated_time_minutes(self):
        return 45

    def __str__(self):
        return self.name


class StandardDelivery(DeliveryType):
    name = "Standard"

    def calculate_charge(self, order_subtotal):
        # Flat fee, free above a threshold.
        if order_subtotal >= 500:
            return 0.0
        return 30.0

    def estimated_time_minutes(self):
        return 45


class ExpressDelivery(DeliveryType):
    name = "Express"

    def calculate_charge(self, order_subtotal):
        # Percentage-based, with a minimum charge.
        charge = order_subtotal * 0.08
        return max(charge, 60.0)

    def estimated_time_minutes(self):
        return 20


class ScheduledDelivery(DeliveryType):
    name = "Scheduled"

    def __init__(self, scheduled_for=None):
        self.scheduled_for = scheduled_for or "later today"

    def calculate_charge(self, order_subtotal):
        # Cheapest option since there's no rush.
        return 15.0

    def estimated_time_minutes(self):
        return 120

    def __str__(self):
        return f"Scheduled ({self.scheduled_for})"


DELIVERY_TYPES = {
    "1": StandardDelivery,
    "2": ExpressDelivery,
    "3": ScheduledDelivery,
}


# ---------------------------------------------------------------------
# Order
# ---------------------------------------------------------------------

class OrderLine:
    """One line item inside an order: a FoodItem + quantity.

    Creating a line checks, in order: quantity is a valid positive int,
    the item hasn't been switched off (`available`), and there's enough
    `stock` left -- then it deducts the stock immediately, so the next
    customer sees an accurate count.
    """

    def __init__(self, food_item, quantity):
        if not isinstance(quantity, int) or quantity <= 0:
            raise InvalidQuantityError(quantity)
        if not food_item.available:
            raise ItemUnavailableError(food_item.name)
        food_item.reduce_stock(quantity)  # raises InsufficientStockError if not enough
        self.food_item = food_item
        self.quantity = quantity

    @property
    def line_total(self):
        return self.food_item.price * self.quantity

    def __str__(self):
        return f"{self.food_item.name} x{self.quantity} = Rs.{self.line_total:.2f}"


class Order:
    """A customer's order from one restaurant, with a delivery strategy."""

    _next_id = 1

    # The only statuses an order can be in, in the order they must occur.
    # CANCELLED can be reached from PLACED or CONFIRMED only (handled in cancel()).
    STATUS_FLOW = ["PLACED", "CONFIRMED", "OUT_FOR_DELIVERY", "DELIVERED"]

    def __init__(
        self,
        customer,
        restaurant,
        delivery_type: DeliveryType,
        order_id=None,
        recipient_name=None,
        recipient_phone=None,
        delivery_address=None,
    ):
        self.order_id = str(order_id) if order_id else str(Order._next_id)
        if order_id is None:
            Order._next_id += 1
        self.customer = customer
        self.restaurant = restaurant
        self.delivery_type = delivery_type
        self.lines = []  # list of OrderLine
        self.timestamp = datetime.now().isoformat(timespec="seconds")
        self.status = "PLACED"

        # Who/where this specific order goes to -- collected at checkout time.
        # Falls back to the customer's saved profile if not given separately
        # (e.g. ordering for someone else, or a different delivery address).
        self.recipient_name = recipient_name or customer.name
        self.recipient_phone = recipient_phone or customer.phone
        self.delivery_address = delivery_address or customer.address

    def advance_status(self):
        """Move the order to the next stage in STATUS_FLOW. Returns the new status."""
        if self.status == "CANCELLED":
            raise InvalidStatusTransitionError(self.status, "advance")
        idx = self.STATUS_FLOW.index(self.status)
        if idx == len(self.STATUS_FLOW) - 1:
            raise InvalidStatusTransitionError(self.status, "further")
        self.status = self.STATUS_FLOW[idx + 1]
        return self.status

    def cancel(self):
        if self.status in ("OUT_FOR_DELIVERY", "DELIVERED", "CANCELLED"):
            raise InvalidStatusTransitionError(self.status, "CANCELLED")
        self.status = "CANCELLED"

    def add_line(self, food_item, quantity):
        line = OrderLine(food_item, quantity)
        self.lines.append(line)
        return line

    @property
    def subtotal(self):
        return sum(line.line_total for line in self.lines)

    @property
    def delivery_charge(self):
        # Polymorphic call: behavior depends on the concrete DeliveryType.
        return self.delivery_type.calculate_charge(self.subtotal)

    @property
    def total(self):
        return self.subtotal + self.delivery_charge

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_id": self.customer.customer_id,
            "restaurant_id": self.restaurant.restaurant_id,
            "delivery_type": self.delivery_type.name,
            "recipient_name": self.recipient_name,
            "recipient_phone": self.recipient_phone,
            "delivery_address": self.delivery_address,
            "items": [
                {"food_id": line.food_item.food_id, "quantity": line.quantity}
                for line in self.lines
            ],
            "subtotal": round(self.subtotal, 2),
            "delivery_charge": round(self.delivery_charge, 2),
            "total": round(self.total, 2),
            "timestamp": self.timestamp,
            "status": self.status,
        }

    def receipt(self):
        lines = [
            f"Order #{self.order_id} - {self.status}",
            f"Deliver to : {self.recipient_name}  ({self.recipient_phone})",
            f"Address    : {self.delivery_address}",
            f"Restaurant: {self.restaurant.name}",
            "-" * 40,
        ]
        for line in self.lines:
            lines.append(f"  {line}")
        lines.append("-" * 40)
        lines.append(f"Subtotal        : Rs.{self.subtotal:.2f}")
        lines.append(f"Delivery ({self.delivery_type}): Rs.{self.delivery_charge:.2f}")
        lines.append(f"TOTAL           : Rs.{self.total:.2f}")
        lines.append(f"ETA             : {self.delivery_type.estimated_time_minutes()} min")
        return "\n".join(lines)
