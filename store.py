# store.py
from __future__ import annotations

from typing import List, Tuple

import products  # make sure products.py (with class Product) is in the same folder


class Store:
    """A Store that holds Product objects and allows multi-item purchases."""

    def __init__(self, products_list: List[products.Product] | None = None):
        self._products: List[products.Product] = list(products_list or [])

    # -------------------- Inventory management --------------------

    def add_product(self, product: products.Product) -> None:
        """Add a product instance to the store."""
        if not isinstance(product, products.Product):
            raise TypeError("add_product expects a Product instance")
        self._products.append(product)

    def remove_product(self, product: products.Product) -> None:
        """Remove a product from the store (if present)."""
        try:
            self._products.remove(product)
        except ValueError:
            # Silently ignore if not found, or raise if you prefer:
            # raise ValueError("Product not found in store")
            pass

    # -------------------- Queries --------------------

    def get_total_quantity(self) -> int:
        """Return the total number of items across all products."""
        return sum(p.get_quantity() for p in self._products)

    def get_all_products(self) -> List[products.Product]:
        """Return all active products."""
        return [p for p in self._products if p.is_active()]

    # -------------------- Ordering --------------------

    def order(self, shopping_list: List[Tuple[products.Product, int]]) -> float:
        """
        Accept a list of (Product, quantity) tuples, validate the request,
        then perform the purchase and return the total price.

        This uses a two-pass approach:
          1) Validate everything (membership, activity, quantity available)
          2) Perform all buys
        to avoid partial orders.
        """
        if not isinstance(shopping_list, list):
            raise TypeError("shopping_list must be a list of (Product, int) tuples")

        # -------- First pass: validate --------
        for item in shopping_list:
            if not (isinstance(item, tuple) and len(item) == 2):
                raise TypeError("Each item must be a tuple: (Product, quantity)")

            prod, qty = item

            if not isinstance(prod, products.Product):
                raise TypeError("First element of each tuple must be a Product instance")
            if not isinstance(qty, int) or qty <= 0:
                raise ValueError("Quantity must be a positive integer")

            if prod not in self._products:
                raise ValueError(f"Product '{prod.name}' is not in this store")
            if not prod.is_active():
                raise ValueError(f"Product '{prod.name}' is inactive")
            if qty > prod.get_quantity():
                raise ValueError(
                    f"Not enough stock for '{prod.name}': requested {qty}, "
                    f"available {prod.get_quantity()}"
                )

        # -------- Second pass: execute buys --------
        total_cost = 0.0
        for prod, qty in shopping_list:
            total_cost += prod.buy(qty)

        return float(total_cost)


# -------------------- Quick manual test --------------------
if __name__ == "__main__":
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        products.Product("Google Pixel 7", price=500, quantity=250),
    ]

    best_buy = Store(product_list)

    # Active products
    active = best_buy.get_all_products()
    print("Active products:", [p.name for p in active])

    # Total quantity in store
    print("Total quantity:", best_buy.get_total_quantity())

    # Place an order using products returned by get_all_products()
    price = best_buy.order([(active[0], 1), (active[1], 2)])
    print(f"Order cost: {price} dollars.")

    # After order, quantities updated:
    for p in active:
        p.show()