# main.py
from __future__ import annotations

import products  # your products.py with class Product
import store     # your store.py with class Store


# ---------------------------------------------------------------------------
# Setup initial stock (default inventory)
# ---------------------------------------------------------------------------
product_list = [
    products.Product("MacBook Air M2", price=1450, quantity=100),
    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    products.Product("Google Pixel 7", price=500, quantity=250),
]
best_buy = store.Store(product_list)


# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------
def _print_menu() -> None:
    print("\n====== Best Buy Store ======")
    print("1. List all products in store")
    print("2. Show total amount in store")
    print("3. Make an order")
    print("4. Quit")


def _list_products(s: store.Store) -> None:
    active = s.get_all_products()
    if not active:
        print("No active products.")
        return
    print("\nActive products:")
    for idx, p in enumerate(active, start=1):
        # mirrors Product.__str__/show
        print(f"{idx}. {p.name} — Price: {p.price:g}, Quantity: {p.get_quantity()}")


def _show_total_amount(s: store.Store) -> None:
    print("\nTotal quantity in store:", s.get_total_quantity())


def _make_order(s: store.Store) -> None:
    active = s.get_all_products()
    if not active:
        print("No active products to order.")
        return

    _list_products(s)
    print("\nEnter items to order. Press ENTER without input to finish.")
    print("Example: choose product number then quantity.")

    shopping_list = []
    while True:
        choice = input("Product # (ENTER to finish): ").strip()
        if choice == "":
            break
        if not choice.isdigit():
            print("Please enter a valid product number.")
            continue

        idx = int(choice)
        if not (1 <= idx <= len(active)):
            print("Product number out of range.")
            continue

        qty_raw = input("Quantity: ").strip()
        if not qty_raw.isdigit():
            print("Please enter a positive integer quantity.")
            continue

        qty = int(qty_raw)
        if qty <= 0:
            print("Quantity must be positive.")
            continue

        shopping_list.append((active[idx - 1], qty))
        print(f"  Added: {active[idx - 1].name} x {qty}")

    if not shopping_list:
        print("No items selected.")
        return

    try:
        total = s.order(shopping_list)
        print(f"\nOrder successful! Total cost: {total:g}")
    except Exception as e:
        print(f"\nOrder failed: {e}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def start(s: store.Store) -> None:
    """Start the interactive menu loop for the given store."""
    while True:
        _print_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            _list_products(s)
        elif choice == "2":
            _show_total_amount(s)
        elif choice == "3":
            _make_order(s)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    # Kick off the UI with the default store
    start(best_buy)