# products.py

class Product:
    def __init__(self, name: str, price: float, quantity: int):
        # basic validation
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("price must be a non-negative number")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("quantity must be a non-negative integer")

        self.name = name.strip()
        self.price = float(price)
        self._quantity = int(quantity)
        self._active = True  # newly created products are active by default
        if self._quantity == 0:
            self._active = False  # 0 in stock means inactive per spec

    # --- getters / setters ---
    def get_quantity(self) -> int:
        return self._quantity

    def set_quantity(self, quantity: int) -> None:
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("quantity must be a non-negative integer")
        self._quantity = quantity
        # If quantity reaches 0, deactivate the product.
        if self._quantity == 0:
            self._active = False

    def is_active(self) -> bool:
        return self._active

    # --- activation controls ---
    def activate(self) -> None:
        self._active = True

    def deactivate(self) -> None:
        self._active = False

    # --- display ---
    def show(self) -> None:
        # e.g. "MacBook Air M2, Price: 1450, Quantity: 100"
        print(f"{self.name}, Price: {self.price:g}, Quantity: {self._quantity}")

    def __str__(self) -> str:
        return f"{self.name}, Price: {self.price:g}, Quantity: {self._quantity}"

    # --- business logic ---
    def buy(self, quantity: int) -> float:
        """
        Buy a given quantity of the product.
        Returns the total price (float).
        Updates the quantity.
        Raises an Exception if:
          - product is inactive
          - quantity requested is not a positive integer
          - not enough quantity in stock
        """
        if not self._active:
            raise Exception("Product is inactive and cannot be purchased.")

        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Requested quantity must be a positive integer.")

        if quantity > self._quantity:
            raise Exception("Insufficient stock for requested quantity.")

        total = self.price * quantity
        self._quantity -= quantity

        if self._quantity == 0:
            # If stock hits 0, deactivate product
            self._active = False

        return float(total)


# --- quick manual test (put in main section if you like) ---
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