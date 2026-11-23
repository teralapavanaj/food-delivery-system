/*
 * FoodFlow UI — a front-end mock-up of the Python Food Delivery
 * Management System (see ../main.py, ../models.py).
 *
 * It mirrors the same domain model so it's a faithful visual of the
 * real logic: FoodItem/Restaurant/Customer, polymorphic delivery
 * charge calculation, stock deduction, and order status tracking.
 * Pure client-side (no backend) — everything resets on page reload,
 * which is expected for a UI demo.
 */

// ---------------------------------------------------------------
// Seed data (mirrors data/restaurants.csv, data/food_items.csv, data/customers.json)
// ---------------------------------------------------------------
const restaurants = [
  { id: "R1", name: "Spice Villa", cuisine: "Indian", rating: 4.5, icon: "🍛" },
  { id: "R2", name: "Pizza Point", cuisine: "Italian", rating: 4.2, icon: "🍕" },
  { id: "R3", name: "Dragon Wok", cuisine: "Chinese", rating: 4.0, icon: "🥡" },
  { id: "R4", name: "Taco Fiesta", cuisine: "Mexican", rating: 4.3, icon: "🌮" },
  { id: "R5", name: "Burger Barn", cuisine: "American", rating: 4.1, icon: "🍔" },
  { id: "R6", name: "Sushi Sensei", cuisine: "Japanese", rating: 4.6, icon: "🍣" },
  { id: "R7", name: "Curry Leaf", cuisine: "South Indian", rating: 4.4, icon: "🥘" },
  { id: "R8", name: "Sweet Treats Bakery", cuisine: "Desserts", rating: 4.7, icon: "🍰" },
  { id: "R9", name: "Green Bowl", cuisine: "Healthy/Salads", rating: 4.2, icon: "🥗" },
  { id: "R10", name: "Brew & Bean", cuisine: "Beverages/Cafe", rating: 4.3, icon: "☕" },
];

const foodItems = [
  { id: "F1", name: "Paneer Butter Masala", category: "Main Course", price: 220, restaurantId: "R1", available: true, stock: 15 },
  { id: "F2", name: "Masala Dosa", category: "Breakfast", price: 90, restaurantId: "R1", available: true, stock: 20 },
  { id: "F3", name: "Gulab Jamun", category: "Dessert", price: 60, restaurantId: "R1", available: true, stock: 2 },
  { id: "F4", name: "Butter Chicken", category: "Main Course", price: 260, restaurantId: "R1", available: true, stock: 12 },
  { id: "F5", name: "Veg Biryani", category: "Main Course", price: 200, restaurantId: "R1", available: true, stock: 10 },
  { id: "F6", name: "Chicken Biryani", category: "Main Course", price: 240, restaurantId: "R1", available: true, stock: 10 },
  { id: "F7", name: "Naan", category: "Bread", price: 35, restaurantId: "R1", available: true, stock: 40 },
  { id: "F8", name: "Tandoori Roti", category: "Bread", price: 25, restaurantId: "R1", available: true, stock: 40 },
  { id: "F9", name: "Samosa", category: "Starter", price: 40, restaurantId: "R1", available: true, stock: 30 },
  { id: "F10", name: "Lassi", category: "Beverage", price: 50, restaurantId: "R1", available: true, stock: 18 },

  { id: "F11", name: "Margherita Pizza", category: "Pizza", price: 260, restaurantId: "R2", available: true, stock: 10 },
  { id: "F12", name: "Pepperoni Pizza", category: "Pizza", price: 320, restaurantId: "R2", available: true, stock: 10 },
  { id: "F13", name: "Garlic Bread", category: "Starter", price: 120, restaurantId: "R2", available: true, stock: 25 },
  { id: "F14", name: "Pasta Alfredo", category: "Main Course", price: 280, restaurantId: "R2", available: true, stock: 9 },
  { id: "F15", name: "Pasta Arrabbiata", category: "Main Course", price: 260, restaurantId: "R2", available: true, stock: 9 },
  { id: "F16", name: "Lasagna", category: "Main Course", price: 310, restaurantId: "R2", available: true, stock: 7 },
  { id: "F17", name: "Tiramisu", category: "Dessert", price: 180, restaurantId: "R2", available: true, stock: 6 },
  { id: "F18", name: "Bruschetta", category: "Starter", price: 150, restaurantId: "R2", available: true, stock: 14 },

  { id: "F19", name: "Veg Hakka Noodles", category: "Main Course", price: 180, restaurantId: "R3", available: true, stock: 12 },
  { id: "F20", name: "Chilli Chicken", category: "Starter", price: 210, restaurantId: "R3", available: true, stock: 8 },
  { id: "F21", name: "Spring Rolls", category: "Starter", price: 140, restaurantId: "R3", available: false, stock: 0 },
  { id: "F22", name: "Manchurian", category: "Starter", price: 170, restaurantId: "R3", available: true, stock: 11 },
  { id: "F23", name: "Fried Rice", category: "Main Course", price: 190, restaurantId: "R3", available: true, stock: 13 },
  { id: "F24", name: "Schezwan Noodles", category: "Main Course", price: 195, restaurantId: "R3", available: true, stock: 10 },
  { id: "F25", name: "Dim Sum", category: "Starter", price: 160, restaurantId: "R3", available: true, stock: 16 },

  { id: "F26", name: "Chicken Tacos", category: "Main Course", price: 230, restaurantId: "R4", available: true, stock: 14 },
  { id: "F27", name: "Veg Burrito", category: "Main Course", price: 210, restaurantId: "R4", available: true, stock: 12 },
  { id: "F28", name: "Nachos", category: "Starter", price: 190, restaurantId: "R4", available: true, stock: 20 },
  { id: "F29", name: "Quesadilla", category: "Main Course", price: 220, restaurantId: "R4", available: true, stock: 10 },
  { id: "F30", name: "Churros", category: "Dessert", price: 130, restaurantId: "R4", available: true, stock: 15 },
  { id: "F31", name: "Guacamole & Chips", category: "Starter", price: 150, restaurantId: "R4", available: true, stock: 18 },

  { id: "F32", name: "Classic Cheeseburger", category: "Main Course", price: 180, restaurantId: "R5", available: true, stock: 22 },
  { id: "F33", name: "Double Patty Burger", category: "Main Course", price: 250, restaurantId: "R5", available: true, stock: 14 },
  { id: "F34", name: "French Fries", category: "Starter", price: 100, restaurantId: "R5", available: true, stock: 35 },
  { id: "F35", name: "Chicken Wings", category: "Starter", price: 220, restaurantId: "R5", available: true, stock: 16 },
  { id: "F36", name: "Onion Rings", category: "Starter", price: 110, restaurantId: "R5", available: true, stock: 20 },
  { id: "F37", name: "Milkshake", category: "Beverage", price: 140, restaurantId: "R5", available: true, stock: 19 },

  { id: "F38", name: "Salmon Nigiri", category: "Main Course", price: 320, restaurantId: "R6", available: true, stock: 8 },
  { id: "F39", name: "California Roll", category: "Main Course", price: 280, restaurantId: "R6", available: true, stock: 10 },
  { id: "F40", name: "Tempura Udon", category: "Main Course", price: 260, restaurantId: "R6", available: true, stock: 9 },
  { id: "F41", name: "Miso Soup", category: "Starter", price: 90, restaurantId: "R6", available: true, stock: 25 },
  { id: "F42", name: "Edamame", category: "Starter", price: 100, restaurantId: "R6", available: true, stock: 22 },
  { id: "F43", name: "Dragon Roll", category: "Main Course", price: 340, restaurantId: "R6", available: true, stock: 7 },

  { id: "F44", name: "Idli Sambar", category: "Breakfast", price: 70, restaurantId: "R7", available: true, stock: 30 },
  { id: "F45", name: "Medu Vada", category: "Breakfast", price: 65, restaurantId: "R7", available: true, stock: 25 },
  { id: "F46", name: "Pongal", category: "Breakfast", price: 80, restaurantId: "R7", available: true, stock: 18 },
  { id: "F47", name: "Rava Dosa", category: "Breakfast", price: 100, restaurantId: "R7", available: true, stock: 16 },
  { id: "F48", name: "Filter Coffee", category: "Beverage", price: 40, restaurantId: "R7", available: true, stock: 40 },
  { id: "F49", name: "Curd Rice", category: "Main Course", price: 90, restaurantId: "R7", available: true, stock: 20 },

  { id: "F50", name: "Chocolate Brownie", category: "Dessert", price: 120, restaurantId: "R8", available: true, stock: 20 },
  { id: "F51", name: "Red Velvet Cake", category: "Dessert", price: 180, restaurantId: "R8", available: true, stock: 12 },
  { id: "F52", name: "Croissant", category: "Bakery", price: 80, restaurantId: "R8", available: true, stock: 25 },
  { id: "F53", name: "Blueberry Muffin", category: "Bakery", price: 90, restaurantId: "R8", available: true, stock: 20 },
  { id: "F54", name: "Cheesecake", category: "Dessert", price: 200, restaurantId: "R8", available: true, stock: 10 },
  { id: "F55", name: "Donut", category: "Bakery", price: 60, restaurantId: "R8", available: true, stock: 30 },

  { id: "F56", name: "Quinoa Salad", category: "Salad", price: 190, restaurantId: "R9", available: true, stock: 15 },
  { id: "F57", name: "Greek Salad", category: "Salad", price: 170, restaurantId: "R9", available: true, stock: 15 },
  { id: "F58", name: "Grilled Chicken Bowl", category: "Main Course", price: 240, restaurantId: "R9", available: true, stock: 12 },
  { id: "F59", name: "Smoothie Bowl", category: "Breakfast", price: 210, restaurantId: "R9", available: true, stock: 10 },
  { id: "F60", name: "Avocado Toast", category: "Breakfast", price: 180, restaurantId: "R9", available: true, stock: 14 },

  { id: "F61", name: "Cold Brew Coffee", category: "Beverage", price: 120, restaurantId: "R10", available: true, stock: 25 },
  { id: "F62", name: "Cappuccino", category: "Beverage", price: 110, restaurantId: "R10", available: true, stock: 25 },
  { id: "F63", name: "Masala Chai", category: "Beverage", price: 45, restaurantId: "R10", available: true, stock: 40 },
  { id: "F64", name: "Iced Tea", category: "Beverage", price: 90, restaurantId: "R10", available: true, stock: 22 },
  { id: "F65", name: "Chocolate Muffin", category: "Bakery", price: 85, restaurantId: "R10", available: true, stock: 18 },
];

const customer = { id: "C1", name: "Shishir", phone: "9999999999", address: "Hyderabad, India" };

// ---------------------------------------------------------------
// Delivery types: polymorphism, mirroring models.py's DeliveryType hierarchy
// ---------------------------------------------------------------
const deliveryTypes = {
  standard: {
    label: "Standard",
    eta: 45,
    calculateCharge(subtotal) { return subtotal >= 500 ? 0 : 30; },
  },
  express: {
    label: "Express",
    eta: 20,
    calculateCharge(subtotal) { return Math.max(subtotal * 0.08, 60); },
  },
  scheduled: {
    label: "Scheduled",
    eta: 120,
    calculateCharge() { return 15; },
  },
};

const STATUS_FLOW = ["PLACED", "CONFIRMED", "OUT_FOR_DELIVERY", "DELIVERED"];

// ---------------------------------------------------------------
// App state
// ---------------------------------------------------------------
let cart = [];          // [{ foodId, quantity }]
let orders = [];         // [{ id, restaurantId, deliveryType, lines, subtotal, deliveryCharge, total, status, placedAt }]
let orderCounter = 1;

// ---------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------
function rupees(n) { return `₹${n.toFixed(2)}`; }
function findFood(id) { return foodItems.find(f => f.id === id); }
function findRestaurant(id) { return restaurants.find(r => r.id === id); }

function toast(message, type = "info") {
  const stack = document.getElementById("toastStack");
  const el = document.createElement("div");
  el.className = `toast ${type}`;
  el.textContent = message;
  stack.appendChild(el);
  setTimeout(() => el.remove(), 3800);
}

// Custom "exceptions" as plain JS errors with a name, mirroring exceptions.py
class InvalidQuantityError extends Error {}
class ItemUnavailableError extends Error {}
class InsufficientStockError extends Error {}

function addToCart(foodId, quantity) {
  const item = findFood(foodId);
  if (!item) throw new Error(`No food item found with ID '${foodId}'.`);
  if (!Number.isInteger(quantity) || quantity <= 0) {
    throw new InvalidQuantityError(`Invalid quantity '${quantity}'. Must be a positive integer.`);
  }
  if (!item.available) {
    throw new ItemUnavailableError(`'${item.name}' is currently unavailable.`);
  }
  const alreadyInCart = cart.filter(l => l.foodId === foodId).reduce((s, l) => s + l.quantity, 0);
  if (quantity + alreadyInCart > item.stock) {
    throw new InsufficientStockError(
      `Only ${item.stock - alreadyInCart} unit(s) of '${item.name}' left in stock (requested ${quantity}).`
    );
  }
  const existing = cart.find(l => l.foodId === foodId);
  if (existing) existing.quantity += quantity;
  else cart.push({ foodId, quantity });
}

function cartRestaurantId() {
  if (cart.length === 0) return null;
  return findFood(cart[0].foodId).restaurantId;
}

function cartSubtotal() {
  return cart.reduce((sum, l) => sum + findFood(l.foodId).price * l.quantity, 0);
}

function selectedDeliveryKey() {
  const el = document.querySelector('input[name="delivery"]:checked');
  return el ? el.value : "standard";
}

// ---------------------------------------------------------------
// Rendering: Restaurants
// ---------------------------------------------------------------
function renderRestaurants() {
  const grid = document.getElementById("restaurantGrid");
  grid.innerHTML = "";
  restaurants.forEach(r => {
    const count = foodItems.filter(f => f.restaurantId === r.id).length;
    const card = document.createElement("div");
    card.className = "restaurant-card";
    card.innerHTML = `
      <span class="count">${count} items</span>
      <div class="cover">${r.icon}</div>
      <h3>${r.name}</h3>
      <div class="cuisine">${r.cuisine} cuisine</div>
      <div class="rating">⭐ ${r.rating.toFixed(1)} / 5</div>
    `;
    card.addEventListener("click", () => {
      switchView("menu");
      document.querySelector('.chip[data-filter="restaurant"]').click();
      document.getElementById("searchInput").value = r.name;
      runSearch();
    });
    grid.appendChild(card);
  });
}

// ---------------------------------------------------------------
// Rendering: Food / Search
// ---------------------------------------------------------------
function stockPillHtml(item) {
  if (!item.available) return `<span class="stock-pill out">Unavailable</span>`;
  if (item.stock <= 0) return `<span class="stock-pill out">Out of stock</span>`;
  if (item.stock <= 4) return `<span class="stock-pill low">${item.stock} left — low stock</span>`;
  return `<span class="stock-pill in">${item.stock} in stock</span>`;
}

function renderFoodGrid(items) {
  const grid = document.getElementById("foodGrid");
  grid.innerHTML = "";
  if (items.length === 0) {
    grid.innerHTML = `<p class="empty-hint">No matching food items.</p>`;
    return;
  }
  items.forEach(item => {
    const restaurant = findRestaurant(item.restaurantId);
    const disabled = !item.available || item.stock <= 0;
    const card = document.createElement("div");
    card.className = "food-card";
    card.innerHTML = `
      <div class="top-row">
        <div>
          <h4>${item.name}</h4>
          <div class="cat">${item.category}</div>
        </div>
        <div class="price">${rupees(item.price)}</div>
      </div>
      <div class="restaurant-tag">${restaurant.icon} ${restaurant.name}</div>
      ${stockPillHtml(item)}
      <div class="add-row">
        <input type="number" min="1" value="1" ${disabled ? "disabled" : ""} id="qty-${item.id}" />
        <button class="btn-add" ${disabled ? "disabled" : ""} data-food="${item.id}">Add to cart</button>
      </div>
    `;
    grid.appendChild(card);
  });

  grid.querySelectorAll(".btn-add").forEach(btn => {
    btn.addEventListener("click", () => {
      const foodId = btn.dataset.food;
      const qtyInput = document.getElementById(`qty-${foodId}`);
      const qty = parseInt(qtyInput.value, 10);
      const item = findFood(foodId);
      const currentRestaurant = cartRestaurantId();

      if (currentRestaurant && currentRestaurant !== item.restaurantId) {
        toast(`Your cart has items from ${findRestaurant(currentRestaurant).name}. Clear cart to order from a different restaurant.`, "error");
        return;
      }
      try {
        addToCart(foodId, qty);
        toast(`Added ${qty} × ${item.name} to cart.`, "success");
        updateCartBadge();
      } catch (e) {
        toast(e.message, "error");
      }
    });
  });
}

function runSearch() {
  const term = document.getElementById("searchInput").value.trim().toLowerCase();
  const filter = document.querySelector(".chip.active").dataset.filter;

  let results = foodItems;
  if (term) {
    results = foodItems.filter(item => {
      const restaurantName = findRestaurant(item.restaurantId).name.toLowerCase();
      if (filter === "name") return item.name.toLowerCase().includes(term);
      if (filter === "category") return item.category.toLowerCase().includes(term);
      if (filter === "restaurant") return restaurantName.includes(term);
      return (
        item.name.toLowerCase().includes(term) ||
        item.category.toLowerCase().includes(term) ||
        restaurantName.includes(term)
      );
    });
  }
  renderFoodGrid(results);
}

// ---------------------------------------------------------------
// Rendering: Cart
// ---------------------------------------------------------------
function renderCart() {
  const linesEl = document.getElementById("cartLines");
  const emptyHint = document.getElementById("cartEmptyHint");
  linesEl.innerHTML = "";

  if (cart.length === 0) {
    emptyHint.style.display = "block";
  } else {
    emptyHint.style.display = "none";
    cart.forEach(line => {
      const item = findFood(line.foodId);
      const row = document.createElement("div");
      row.className = "cart-line";
      row.innerHTML = `
        <div>
          <div class="name">${item.name} × ${line.quantity}</div>
          <div class="meta">${rupees(item.price)} each · ${rupees(item.price * line.quantity)}</div>
        </div>
        <button class="remove" data-food="${line.foodId}">Remove</button>
      `;
      linesEl.appendChild(row);
    });
    linesEl.querySelectorAll(".remove").forEach(btn => {
      btn.addEventListener("click", () => {
        cart = cart.filter(l => l.foodId !== btn.dataset.food);
        renderCart();
        updateCartBadge();
      });
    });
  }
  updateCartSummary();
}

function updateCartSummary() {
  const subtotal = cartSubtotal();
  const deliveryKey = selectedDeliveryKey();
  const charge = deliveryTypes[deliveryKey].calculateCharge(subtotal);
  document.getElementById("sumSubtotal").textContent = rupees(subtotal);
  document.getElementById("sumDelivery").textContent = rupees(charge);
  document.getElementById("sumTotal").textContent = rupees(subtotal + charge);
  document.getElementById("placeOrderBtn").disabled = cart.length === 0;
}

function updateCartBadge() {
  const count = cart.reduce((s, l) => s + l.quantity, 0);
  document.getElementById("cartBadge").textContent = count;
}

// ---------------------------------------------------------------
// Placing an order
// ---------------------------------------------------------------
function validateDeliveryDetails() {
  const nameEl = document.getElementById("recipientName");
  const phoneEl = document.getElementById("recipientPhone");
  const addressEl = document.getElementById("recipientAddress");
  const fields = [nameEl, phoneEl, addressEl];
  fields.forEach(el => el.classList.remove("invalid"));

  const name = nameEl.value.trim();
  const phone = phoneEl.value.trim();
  const address = addressEl.value.trim();

  const missing = [];
  if (!name) { missing.push("recipient name"); nameEl.classList.add("invalid"); }
  if (!phone) { missing.push("phone number"); phoneEl.classList.add("invalid"); }
  if (!address) { missing.push("delivery address"); addressEl.classList.add("invalid"); }

  if (missing.length > 0) {
    toast(`Please fill in: ${missing.join(", ")}.`, "error");
    return null;
  }
  return { name, phone, address };
}

function placeOrder() {
  if (cart.length === 0) return;
  const details = validateDeliveryDetails();
  if (!details) return;

  const restaurantId = cartRestaurantId();
  const restaurant = findRestaurant(restaurantId);
  const deliveryKey = selectedDeliveryKey();
  const delivery = deliveryTypes[deliveryKey];

  // Deduct stock now (mirrors OrderLine.__init__ in models.py)
  for (const line of cart) {
    const item = findFood(line.foodId);
    item.stock -= line.quantity;
  }

  const subtotal = cartSubtotal_fromLines(cart);
  const charge = delivery.calculateCharge(subtotal);

  const order = {
    id: String(orderCounter++),
    restaurantName: restaurant.name,
    deliveryLabel: delivery.label,
    eta: delivery.eta,
    recipientName: details.name,
    recipientPhone: details.phone,
    deliveryAddress: details.address,
    lines: cart.map(l => ({ name: findFood(l.foodId).name, qty: l.quantity, price: findFood(l.foodId).price })),
    subtotal,
    deliveryCharge: charge,
    total: subtotal + charge,
    status: "PLACED",
    placedAt: new Date().toLocaleString(),
  };
  orders.unshift(order);
  cart = [];
  renderCart();
  updateCartBadge();
  renderOrders();
  toast(`Order #${order.id} placed — track it under "Track Orders".`, "success");
  switchView("orders");
}

function cartSubtotal_fromLines(lines) {
  return lines.reduce((sum, l) => sum + findFood(l.foodId).price * l.quantity, 0);
}

// ---------------------------------------------------------------
// Rendering: Orders / tracking
// ---------------------------------------------------------------
function renderOrders() {
  const list = document.getElementById("ordersList");
  const emptyHint = document.getElementById("ordersEmptyHint");
  list.innerHTML = "";

  if (orders.length === 0) {
    emptyHint.style.display = "block";
  } else {
    emptyHint.style.display = "none";
    orders.forEach(order => list.appendChild(buildOrderCard(order)));
  }
  renderCustomerHistory();
}

function buildOrderCard(order) {
  const card = document.createElement("div");
  card.className = "order-card";

  const flowIndex = STATUS_FLOW.indexOf(order.status);
  const isCancelled = order.status === "CANCELLED";

  const stepsHtml = STATUS_FLOW.map((status, i) => {
    const done = !isCancelled && i <= flowIndex;
    return `
      <div class="progress-step ${done ? "done" : ""}">
        <div class="dot"></div>
        <span class="lbl">${status.replace(/_/g, " ")}</span>
      </div>`;
  }).join("");

  const itemsSummary = order.lines.map(l => `${l.name} ×${l.qty}`).join(", ");
  const recipientLine = order.recipientName
    ? `Deliver to <strong style="color:var(--text)">${order.recipientName}</strong> (${order.recipientPhone}) · ${order.deliveryAddress}`
    : "";

  const canAdvance = !isCancelled && flowIndex < STATUS_FLOW.length - 1;
  const canCancel = !isCancelled && order.status !== "OUT_FOR_DELIVERY" && order.status !== "DELIVERED";

  card.innerHTML = `
    <div class="order-top">
      <strong>Order #${order.id} · ${order.restaurantName}</strong>
      <span class="status-tag status-${order.status}">${order.status.replace(/_/g, " ")}</span>
    </div>
    ${isCancelled ? "" : `<div class="progress-track">${stepsHtml}</div>`}
    ${recipientLine ? `<div class="order-items">${recipientLine}</div>` : ""}
    <div class="order-items">${itemsSummary}</div>
    <div class="order-items">
      Subtotal ${rupees(order.subtotal)} · ${order.deliveryLabel} delivery ${rupees(order.deliveryCharge)}
      · <strong style="color:var(--text)">Total ${rupees(order.total)}</strong> · ETA ${order.eta} min
    </div>
    <div class="order-actions">
      <button class="btn-ghost" data-action="advance" data-id="${order.id}" ${canAdvance ? "" : "disabled"}>Advance status →</button>
      <button class="btn-ghost danger" data-action="cancel" data-id="${order.id}" ${canCancel ? "" : "disabled"}>Cancel order</button>
    </div>
  `;

  card.querySelector('[data-action="advance"]').addEventListener("click", () => advanceOrder(order.id));
  card.querySelector('[data-action="cancel"]').addEventListener("click", () => cancelOrder(order.id));
  return card;
}

function advanceOrder(id) {
  const order = orders.find(o => o.id === id);
  if (!order) { toast(`No order found with ID '${id}'.`, "error"); return; }
  const idx = STATUS_FLOW.indexOf(order.status);
  if (order.status === "CANCELLED" || idx === STATUS_FLOW.length - 1) {
    toast(`Cannot move order from '${order.status}' any further.`, "error");
    return;
  }
  order.status = STATUS_FLOW[idx + 1];
  toast(`Order #${id} is now ${order.status.replace(/_/g, " ")}.`, "success");
  renderOrders();
}

function cancelOrder(id) {
  const order = orders.find(o => o.id === id);
  if (!order) { toast(`No order found with ID '${id}'.`, "error"); return; }
  if (order.status === "OUT_FOR_DELIVERY" || order.status === "DELIVERED") {
    toast(`Cannot cancel order from '${order.status}'.`, "error");
    return;
  }
  order.status = "CANCELLED";
  toast(`Order #${id} cancelled.`, "success");
  renderOrders();
}

function renderCustomerHistory() {
  const el = document.getElementById("customerHistory");
  if (!el) return;
  el.innerHTML = "";
  if (orders.length === 0) {
    el.innerHTML = `<p class="empty-hint">No past orders.</p>`;
    return;
  }
  orders.forEach(order => el.appendChild(buildOrderCard(order)));
}

// ---------------------------------------------------------------
// Navigation
// ---------------------------------------------------------------
function switchView(view) {
  document.querySelectorAll(".nav-item").forEach(btn => btn.classList.toggle("active", btn.dataset.view === view));
  document.querySelectorAll(".view").forEach(sec => sec.classList.toggle("active", sec.id === `view-${view}`));
}

// ---------------------------------------------------------------
// Init
// ---------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".nav-item").forEach(btn => {
    btn.addEventListener("click", () => switchView(btn.dataset.view));
  });

  document.querySelectorAll(".chip").forEach(chip => {
    chip.addEventListener("click", () => {
      document.querySelectorAll(".chip").forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      runSearch();
    });
  });

  document.getElementById("searchInput").addEventListener("input", runSearch);
  document.querySelectorAll('input[name="delivery"]').forEach(r => r.addEventListener("change", updateCartSummary));
  document.getElementById("placeOrderBtn").addEventListener("click", placeOrder);

  // Pre-fill delivery details with the customer's saved profile (editable).
  document.getElementById("recipientName").value = customer.name;
  document.getElementById("recipientPhone").value = customer.phone;
  document.getElementById("recipientAddress").value = customer.address;

  renderRestaurants();
  renderFoodGrid(foodItems);
  renderCart();
  renderOrders();
  updateCartBadge();
});
