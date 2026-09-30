"""Episode 5 — ABC vs Protocol. Run: python payments.py"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount: int, currency: str) -> str:
        """Amount is integer minor units (cents)."""


class StripeProcessor(PaymentProcessor):
    def __init__(self, merchant: str) -> None:
        self.merchant = merchant

    def charge(self, amount: int, currency: str) -> str:
        return f"stripe:{self.merchant}:{amount}{currency}"


class PaypalProcessor(PaymentProcessor):
    def charge(self, amount: int, currency: str) -> str:
        return f"paypal:{amount}{currency}"


@runtime_checkable
class Chargeable(Protocol):
    def charge(self, amount: int, currency: str) -> str: ...


class GiftCard:
    def __init__(self, remaining: int) -> None:
        self.remaining = remaining

    def charge(self, amount: int, currency: str) -> str:
        if amount > self.remaining:
            raise ValueError("gift card empty")
        self.remaining -= amount
        return f"gift:{amount}{currency}"


def checkout(processor: PaymentProcessor, amount: int) -> str:
    return processor.charge(amount, "USD")


def checkout_duck(processor: Chargeable, amount: int) -> str:
    return processor.charge(amount, "USD")


def main() -> None:
    stripe = StripeProcessor("acct_ada")
    paypal = PaypalProcessor()
    print(checkout(stripe, 1999))
    print(checkout(paypal, 500))
    print("stripe is PaymentProcessor:", isinstance(stripe, PaymentProcessor))

    card = GiftCard(5000)
    print("gift card is PaymentProcessor:", isinstance(card, PaymentProcessor))
    print("gift card is Chargeable:", isinstance(card, Chargeable))
    print(checkout_duck(card, 250))
    print(checkout_duck(stripe, 250))

    try:
        PaymentProcessor()  # type: ignore[abstract]
    except TypeError as exc:
        print("abstract:", type(exc).__name__, "- missing charge")


if __name__ == "__main__":
    main()
