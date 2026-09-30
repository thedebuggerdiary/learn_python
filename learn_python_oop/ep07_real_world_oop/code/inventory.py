"""Episode 7 — dataclasses domain model. Used by test_inventory.py and as a script."""

from dataclasses import dataclass, field
from enum import Enum


class Status(Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class Money:
    cents: int
    currency: str = "USD"

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("currency mismatch")
        return Money(self.cents + other.cents, self.currency)

    def __mul__(self, n: int) -> "Money":
        return Money(self.cents * n, self.currency)

    def __rmul__(self, n: int) -> "Money":
        return self.__mul__(n)


@dataclass
class Product:
    sku: str
    name: str
    unit_price: Money
    stock: int = 0

    def allocate(self, qty: int) -> None:
        if qty > self.stock:
            raise ValueError(f"only {self.stock} in stock for {self.sku}")
        self.stock -= qty


@dataclass
class LineItem:
    product: Product
    qty: int

    def total(self) -> Money:
        return self.product.unit_price * self.qty


class PrintableMixin:
    """Small behavior mixin — contrast with Order composing LineItem objects."""

    def summary(self) -> str:
        order_id = getattr(self, "order_id", "?")
        return f"{type(self).__name__}({order_id})"


@dataclass
class Order(PrintableMixin):
    order_id: str
    status: Status = Status.PENDING
    lines: list[LineItem] = field(default_factory=list)

    def add(self, product: Product, qty: int) -> None:
        product.allocate(qty)
        self.lines.append(LineItem(product, qty))

    def total(self) -> Money:
        total = Money(0)
        for line in self.lines:
            total = total + line.total()
        return total

    def pay(self) -> None:
        if self.status is not Status.PENDING:
            raise ValueError(f"cannot pay from {self.status}")
        self.status = Status.PAID


def main() -> None:
    mug = Product("SKU-MUG", "Mug", Money(1299), stock=10)
    tea = Product("SKU-TEA", "Tea", Money(499), stock=50)
    order = Order("ORD-1")
    order.add(mug, 2)
    order.add(tea, 3)
    print(order.summary())
    print("total cents:", order.total().cents)
    order.pay()
    print("status:", order.status)
    print("mug stock:", mug.stock)


if __name__ == "__main__":
    main()
