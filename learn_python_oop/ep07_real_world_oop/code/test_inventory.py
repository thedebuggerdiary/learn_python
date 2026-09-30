"""Episode 7 — pytest suite. From this directory: python -m pytest test_inventory.py"""

import pytest

from inventory import Money, Order, Product, Status


def test_money_adds_and_multiplies() -> None:
    assert Money(100) + Money(50) == Money(150)
    assert 3 * Money(10) == Money(30)


def test_money_rejects_currency_mismatch() -> None:
    with pytest.raises(ValueError, match="currency mismatch"):
        Money(1, "USD") + Money(1, "EUR")


def test_frozen_money_cannot_mutate() -> None:
    from dataclasses import FrozenInstanceError

    m = Money(100)
    with pytest.raises(FrozenInstanceError):
        m.cents = 0  # type: ignore[misc]


def test_order_allocates_stock_and_totals() -> None:
    mug = Product("SKU-MUG", "Mug", Money(1299), stock=10)
    order = Order("ORD-1")
    order.add(mug, 2)
    assert mug.stock == 8
    assert order.total() == Money(2598)
    assert order.status is Status.PENDING


def test_order_pay_is_a_state_machine() -> None:
    mug = Product("SKU-MUG", "Mug", Money(100), stock=1)
    order = Order("ORD-2")
    order.add(mug, 1)
    order.pay()
    assert order.status is Status.PAID
    with pytest.raises(ValueError, match="cannot pay"):
        order.pay()


def test_allocate_rejects_over_stock() -> None:
    mug = Product("SKU-MUG", "Mug", Money(100), stock=1)
    order = Order("ORD-3")
    with pytest.raises(ValueError, match="only 1 in stock"):
        order.add(mug, 2)
