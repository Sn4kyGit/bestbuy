# main.py
"""CLI user interface for the Best Buy store example."""

from __future__ import annotations

from typing import List, Tuple

import products  # products.py with class Product
import store     # store.py with class Store


# ---------------------------------------------------------------------------
# Setup initial stock (default inventory)
# ---------------------------------------------------------------------------
product_list: List[products.Product] = [
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
    for idx, prod in enumerate(active, start=1):
        print(f"{idx}. {prod.name} — Price: {prod.price:g}, "
              f"Quantity: {prod.get_quantity()}")


def _show_total_amount(s: store.Store) -> None:
    print("\nTotal quantity in store:", s.get_total_quantity())


def _prompt_positive_int(prompt: str) -> int | None:
    raw = input(prompt).strip()
    if raw == "":
        return None
    if not raw.isdigit():
        print("Please enter a positive integer.")
        return 0
    value = int(raw)
    if value <= 0:
        print("Please enter a positive integer.")
        return 0
    return value


def _make_order(s: store.Store) -> None:
    active = s.get_all_products()
    if not active:
        print("No active products to order.")
        return

    _list_products(s)
    print("\nEnter items to order. Press ENTER on product number to finish.")

    shopping_list: List[Tuple[products.Product, int]] = []
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

        qty = _prompt_positive_int("Quantity: ")
        if qty is None:
            print("Quantity is required.")
            continue
        if qty == 0:
            continue

        product = active[idx - 1]
        shopping_list.append((product, qty))
        print(f"  Added: {product.name} x {qty}")

    if not shopping_list:
        print("No items selected.")
        return

    try:
        total = s.order(shopping_list)
        print(f"\nOrder successful! Total cost: {total:g}")
    except Exception as exc:
        print(f"\nOrder failed: {exc}")


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
    start(best_buy)