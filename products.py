# products.py
"""Product entity for a simple store system."""

from __future__ import annotations


class Product:
    """Represents a product with name, price, quantity and active state."""

    def __init__(self, name: str, price: float, quantity: int) -> None:
        # basic validation
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("price must be a non-negative number")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("quantity must be a non-negative integer")

        self.name: str = name.strip()
        self.price: float = float(price)
        self._quantity: int = int(quantity)
        self._active: bool = self._quantity > 0

    # -------------------- getters / setters --------------------

    def get_quantity(self) -> int:
        """Return current quantity."""
        return self._quantity

    def set_quantity(self, quantity: int) -> None:
        """Set quantity; deactivates the product when it reaches 0."""
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("quantity must be a non-negative integer")
        self._quantity = quantity
        if self._quantity == 0:
            self._active = False

    def is_active(self) -> bool:
        """Return True if the product is active, else False."""
        return self._active

    # -------------------- activation controls --------------------

    def activate(self) -> None:
        """Activate the product."""
        self._active = True

    def deactivate(self) -> None:
        """Deactivate the product."""
        self._active = False

    # -------------------- display --------------------

    def show(self) -> None:
        """Print a human-readable description of the product."""
        print(f"{self.name}, Price: {self.price:g}, Quantity: {self._quantity}")

    def __str__(self) -> str:  # pragma: no cover - convenience
        return f"{self.name}, Price: {self.price:g}, Quantity: {self._quantity}"

    # -------------------- business logic --------------------

    def buy(self, quantity: int) -> float:
        """
        Buy a given quantity of the product.

        Returns:
            float: total price of the purchase.

        Raises:
            Exception: if product is inactive or insufficient stock.
            ValueError: if requested quantity is not a positive integer.
        """
        if not self._active:
            raise Exception("Product is inactive and cannot be purchased.")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("requested quantity must be a positive integer")
        if quantity > self._quantity:
            raise Exception("insufficient stock for requested quantity")

        total = self.price * quantity
        self._quantity -= quantity

        if self._quantity == 0:
            self._active = False

        return float(total)


# -------------------- quick manual test --------------------
if __name__ == "__main__":
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    bose.show()
    mac.show()

    bose.set_quantity(1000)
    bose.show()