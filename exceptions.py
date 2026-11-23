"""
Custom exceptions for the Food Delivery Management System.

Keeping these in one module makes it easy to catch specific
failure modes (bad IDs, unavailable items, bad quantities, file
problems) instead of bare `except Exception`.
"""


class FoodDeliveryError(Exception):
    """Base class for all application-specific errors."""
    pass


class InvalidFoodIDError(FoodDeliveryError):
    """Raised when a food item ID does not exist in the system."""

    def __init__(self, food_id):
        self.food_id = food_id
        super().__init__(f"No food item found with ID '{food_id}'.")


class InvalidRestaurantIDError(FoodDeliveryError):
    """Raised when a restaurant ID does not exist in the system."""

    def __init__(self, restaurant_id):
        self.restaurant_id = restaurant_id
        super().__init__(f"No restaurant found with ID '{restaurant_id}'.")


class InvalidCustomerIDError(FoodDeliveryError):
    """Raised when a customer ID does not exist in the system."""

    def __init__(self, customer_id):
        self.customer_id = customer_id
        super().__init__(f"No customer found with ID '{customer_id}'.")


class ItemUnavailableError(FoodDeliveryError):
    """Raised when a food item exists but is currently unavailable."""

    def __init__(self, food_name):
        self.food_name = food_name
        super().__init__(f"'{food_name}' is currently unavailable.")


class InvalidQuantityError(FoodDeliveryError):
    """Raised when an order quantity is not a positive integer."""

    def __init__(self, quantity):
        self.quantity = quantity
        super().__init__(
            f"Invalid quantity '{quantity}'. Quantity must be a positive integer."
        )


class InsufficientStockError(FoodDeliveryError):
    """Raised when the requested quantity exceeds what's left in stock."""

    def __init__(self, food_name, requested, in_stock):
        self.food_name = food_name
        self.requested = requested
        self.in_stock = in_stock
        super().__init__(
            f"Only {in_stock} unit(s) of '{food_name}' left in stock "
            f"(requested {requested})."
        )


class InvalidOrderIDError(FoodDeliveryError):
    """Raised when an order ID does not exist in the system."""

    def __init__(self, order_id):
        self.order_id = order_id
        super().__init__(f"No order found with ID '{order_id}'.")


class InvalidStatusTransitionError(FoodDeliveryError):
    """Raised when an order status change doesn't follow the allowed sequence."""

    def __init__(self, current_status, attempted_status):
        self.current_status = current_status
        self.attempted_status = attempted_status
        super().__init__(
            f"Cannot move order from '{current_status}' to '{attempted_status}'."
        )


class FileOperationError(FoodDeliveryError):
    """Raised when reading/writing a CSV or JSON data file fails."""

    def __init__(self, filename, reason):
        self.filename = filename
        self.reason = reason
        super().__init__(f"File operation failed for '{filename}': {reason}")


class InvalidContactDetailsError(FoodDeliveryError):
    """Raised when a phone number or address fails validation."""

    def __init__(self, field, reason):
        self.field = field
        self.reason = reason
        super().__init__(f"Invalid {field}: {reason}.")


class InvalidScheduleError(FoodDeliveryError):
    """Raised when a scheduled delivery time is malformed or in the past."""

    def __init__(self, reason):
        self.reason = reason
        super().__init__(f"Invalid schedule: {reason}.")