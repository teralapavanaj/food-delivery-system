"""
Food Delivery Management System, CLI prototype.

Run:  python main.py

Menu-driven console app that ties together:
  - FoodItem / Restaurant / Customer (models.py)
  - Order + polymorphic DeliveryType hierarchy (models.py)
  - CSV/JSON persistence with error handling (data_manager.py)
  - Custom exceptions (exceptions.py)
"""

from data_manager import DataManager
from models import (
    Customer,
    Order,
    DELIVERY_TYPES,
    ScheduledDelivery,
    StandardDelivery,
    parse_schedule,
    validate_phone,
    validate_address,
)
from exceptions import (
    FoodDeliveryError,
    InvalidRestaurantIDError,
    InvalidCustomerIDError,
    InvalidOrderIDError,
)


def print_menu():
    print(
        """
==================== FOOD DELIVERY MANAGEMENT SYSTEM ====================
1. List restaurants
2. Search food items (by name, category, or restaurant)
3. View a restaurant's menu
4. Register a new customer
5. Place an order
6. View customer order history
7. Check / update order status (track delivery)
0. Exit
===========================================================================
"""
    )


def list_restaurants(dm: DataManager):
    if not dm.restaurants:
        print("No restaurants on file.")
        return
    for r in dm.restaurants.values():
        print(" ", r)


def search_food_items(dm: DataManager):
    print("Search by: 1) Name  2) Category  3) Restaurant")
    mode = input("Choose [1-3] (blank = search name+category): ").strip()
    term = input("Search term (blank = show all): ").strip().lower()

    def restaurant_matches(item, term):
        restaurant = dm.restaurants.get(item.restaurant_id)
        if restaurant is None:
            return False
        return term in restaurant.name.lower() or term == restaurant.restaurant_id.lower()

    if mode == "1":
        results = [item for item in dm.food_items.values() if term in item.name.lower()]
    elif mode == "2":
        results = [item for item in dm.food_items.values() if term in item.category.lower()]
    elif mode == "3":
        results = [item for item in dm.food_items.values() if restaurant_matches(item, term)]
    else:
        results = [
            item for item in dm.food_items.values()
            if term in item.name.lower() or term in item.category.lower()
        ]

    if not results:
        print("No matching food items.")
        return
    for item in results:
        restaurant = dm.restaurants.get(item.restaurant_id)
        rname = restaurant.name if restaurant else item.restaurant_id
        print(f"  {item}  @ {rname}")


def view_menu(dm: DataManager):
    rid = input("Restaurant ID: ").strip()
    restaurant = dm.restaurants.get(rid)
    if restaurant is None:
        raise InvalidRestaurantIDError(rid)
    print(f"\nMenu for {restaurant.name}:")
    if not restaurant.menu:
        print("  (no items)")
    for item in restaurant.menu:
        print(" ", item)


def register_customer(dm: DataManager):
    cid = input("New customer ID: ").strip()
    if cid in dm.customers:
        print("That customer ID already exists.")
        return
    name = input("Name: ").strip()
    phone = validate_phone(input("Phone: ").strip())
    address = validate_address(input("Address: ").strip())
    customer = Customer(cid, name, phone, address)
    dm.customers[cid] = customer
    dm.save_customers()
    print(f"Registered customer {customer}.")


def _get_or_register_customer(dm: DataManager, cid):
    """Look up a customer by ID. If they don't exist yet, collect their
    details right here instead of forcing a separate 'register' step first."""
    customer = dm.customers.get(cid)
    if customer is not None:
        return customer

    print(f"No customer with ID '{cid}' yet, let's register you.")
    name = input("  Your name: ").strip()
    phone = validate_phone(input("  Phone number: ").strip())
    address = validate_address(input("  Address: ").strip())
    if not name:
        raise InvalidCustomerIDError(cid)
    customer = Customer(cid, name, phone, address)
    dm.customers[cid] = customer
    dm.save_customers()
    print(f"Registered customer {customer}.\n")
    return customer


def place_order(dm: DataManager):
    cid = input("Customer ID (new ID to register on the spot): ").strip()
    customer = _get_or_register_customer(dm, cid)

    rid = input("Restaurant ID: ").strip()
    restaurant = dm.restaurants.get(rid)
    if restaurant is None:
        raise InvalidRestaurantIDError(rid)

    print(f"\nMenu for {restaurant.name}:")
    for item in restaurant.menu:
        print(" ", item)

    print("\nDelivery type: 1) Standard  2) Express  3) Scheduled")
    choice = input("Choose delivery type [1-3]: ").strip()
    if choice == "3":
        when = input("Delivery date and time (YYYY-MM-DD HH:MM): ")
        delivery_type = ScheduledDelivery(parse_schedule(when))
    else:
        delivery_cls = DELIVERY_TYPES.get(choice)
        if delivery_cls is None:
            print("Invalid choice, defaulting to Standard.")
            delivery_cls = StandardDelivery
        delivery_type = delivery_cls()

    print("\nWho should this order be delivered to? (blank = use your saved details)")
    recipient_name = input(f"  Recipient name [{customer.name}]: ").strip() or customer.name
    recipient_phone = input(f"  Phone [{customer.phone}]: ").strip() or customer.phone
    delivery_address = input(f"  Delivery address [{customer.address}]: ").strip() or customer.address

    # Validate before any stock is deducted, so bad details cannot leave stock reduced.
    recipient_phone = validate_phone(recipient_phone)
    delivery_address = validate_address(delivery_address)

    order = Order(
        customer, restaurant, delivery_type,
        recipient_name=recipient_name,
        recipient_phone=recipient_phone,
        delivery_address=delivery_address,
    )

    while True:
        food_id = input("\nFood ID to add (blank to finish order): ").strip()
        if not food_id:
            break
        try:
            item = dm.get_food_item(food_id, restaurant.restaurant_id)  # D-06
            qty_raw = input(f"Quantity of '{item.name}' (in stock: {item.stock}): ").strip()
            qty = int(qty_raw) if qty_raw.lstrip("-").isdigit() else -1
            order.add_line(item, qty)
            print(f"  Added: {item.name} x{qty}")
        except FoodDeliveryError as e:
            print(f"  Error: {e}")

    if not order.lines:
        print("Order cancelled: no items added.")
        return

    order.order_id = dm.next_order_id()  # D-01: assigned only when the order is kept
    customer.order_history.append(order.order_id)
    dm.save_order(order)
    dm.save_customers()
    dm.save_food_items()

    print("\n" + order.receipt())
    print(f"Track this order anytime with option 7, Order ID: {order.order_id}")


def view_order_history(dm: DataManager):
    cid = input("Customer ID: ").strip()
    customer = dm.customers.get(cid)
    if customer is None:
        raise InvalidCustomerIDError(cid)
    if not customer.order_history:
        print("No past orders.")
        return
    print(f"Order IDs for {customer.name}: {', '.join(customer.order_history)}")


def track_order(dm: DataManager):
    order_id = input("Order ID: ").strip()
    record = dm.get_order_status(order_id)  # raises InvalidOrderIDError if not found
    print(f"\nOrder #{record['order_id']}, current status: {record['status']}")
    print(f"  Flow: {' -> '.join(Order.STATUS_FLOW)}")

    if record["status"] in ("DELIVERED", "CANCELLED"):
        print("This order is already final; no further updates possible.")
        return

    action = input(
        "\n[Enter]=just view, 'n'=advance to next stage, 'c'=cancel order: "
    ).strip().lower()
    if action == "n":
        updated = dm.update_order_status(order_id)  # advances one step
        print(f"Order #{order_id} is now: {updated['status']}")
    elif action == "c":
        dm.update_order_status(order_id, new_status="CANCELLED")
        print(f"Order #{order_id} has been cancelled and its stock restored.")


def main():
    dm = DataManager(data_dir="data")
    try:
        dm.load_all()
    except FoodDeliveryError as e:
        print(f"Startup error: {e}")
        print("Make sure the 'data' folder with restaurants.csv and food_items.csv exists.")
        return

    print(
        f"Loaded {len(dm.restaurants)} restaurants, "
        f"{len(dm.food_items)} food items, {len(dm.customers)} customers."
    )

    actions = {
        "1": list_restaurants,
        "2": search_food_items,
        "3": view_menu,
        "4": register_customer,
        "5": place_order,
        "6": view_order_history,
        "7": track_order,
    }

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid option, try again.")
            continue
        try:
            action(dm)
        except FoodDeliveryError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Invalid input: {e}")


if __name__ == "__main__":
    main()