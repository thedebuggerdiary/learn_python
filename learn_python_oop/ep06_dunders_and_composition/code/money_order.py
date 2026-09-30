"""Episode 6 — dunders and composition. Run: python money_order.py"""

from __future__ import annotations


class Money:
    def __init__(self, cents: int, currency: str = "USD") -> None:
        if currency != "USD":
            raise ValueError("only USD in this demo")
        self._cents = int(cents)
        self.currency = currency

    @classmethod
    def from_dollars(cls, dollars: float) -> Money:
        return cls(round(dollars * 100))

    @property
    def cents(self) -> int:
        return self._cents

    def __repr__(self) -> str:
        return f"Money({self._cents}, {self.currency!r})"

    def __str__(self) -> str:
        sign = "-" if self._cents < 0 else ""
        whole, frac = divmod(abs(self._cents), 100)
        return f"{sign}${whole}.{frac:02d}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self._cents == other._cents and self.currency == other.currency

    def __hash__(self) -> int:
        return hash((self._cents, self.currency))

    def __add__(self, other: Money) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        if other.currency != self.currency:
            raise ValueError("currency mismatch")
        return Money(self._cents + other._cents, self.currency)

    def __mul__(self, n: int) -> Money:
        if not isinstance(n, int):
            return NotImplemented
        return Money(self._cents * n, self.currency)

    def __rmul__(self, n: int) -> Money:
        return self.__mul__(n)


class LineItem:
    def __init__(self, sku: str, unit_price: Money, qty: int) -> None:
        self.sku = sku
        self.unit_price = unit_price
        self.qty = qty

    def total(self) -> Money:
        return self.unit_price * self.qty

    def __repr__(self) -> str:
        return f"LineItem({self.sku!r}, {self.unit_price!r}, {self.qty})"


class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id = order_id
        self._items: list[LineItem] = []

    def add(self, item: LineItem) -> None:
        self._items.append(item)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def total(self) -> Money:
        total = Money(0)
        for item in self:
            total = total + item.total()
        return total

    def __repr__(self) -> str:
        return f"Order({self.order_id!r}, items={list(self)!r})"


def main() -> None:
    price = Money.from_dollars(12.50)
    print("repr:", repr(price))
    print("str:", price)
    print("eq:", price == Money(1250))
    bag = {price, Money(1250), Money(100)}
    print("hashable set size:", len(bag))
    print("contains 100 cents:", Money(100) in bag)

    item = LineItem("SKU-1", price, 2)
    print("line total:", item.total())

    order = Order("ORD-9")
    order.add(item)
    order.add(LineItem("SKU-2", Money(199), 1))
    print("len:", len(order))
    print("skus:", [line.sku for line in order])
    print("order total:", order.total())
    print("3 * price:", 3 * price)


if __name__ == "__main__":
    main()
