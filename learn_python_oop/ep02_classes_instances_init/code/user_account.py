"""Episode 2 — instance vs class attributes. Run: python user_account.py"""


class User:
    roles: list[str] = ["viewer"]

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email

    @classmethod
    def from_email(cls, email: str) -> "User":
        local = email.split("@", 1)[0]
        return cls(name=local, email=email)

    @staticmethod
    def is_valid_email(email: str) -> bool:
        return "@" in email and "." in email.split("@", 1)[-1]

    def __repr__(self) -> str:
        return f"User(name={self.name!r}, email={self.email!r})"


class Account:
    def __init__(self, owner: User, number: str) -> None:
        self.owner = owner
        self.number = number
        self.transactions: list[tuple[str, float]] = []

    def record(self, kind: str, amount: float) -> None:
        self.transactions.append((kind, amount))

    def __repr__(self) -> str:
        return f"Account(number={self.number!r}, n={len(self.transactions)})"


class BrokenAccount:
    transactions: list[tuple[str, float]] = []

    def __init__(self, owner: User, number: str) -> None:
        self.owner = owner
        self.number = number

    def record(self, kind: str, amount: float) -> None:
        self.transactions.append((kind, amount))


def main() -> None:
    print("valid email:", User.is_valid_email("ada@example.com"))
    ada = User.from_email("ada@example.com")
    print("from_email:", ada)

    good_a = Account(ada, "A-1")
    good_b = Account(User("Grace", "grace@example.com"), "B-2")
    good_a.record("deposit", 25)
    print("good A:", good_a.transactions)
    print("good B:", good_b.transactions)

    bad_a = BrokenAccount(ada, "A-1")
    bad_b = BrokenAccount(User("Grace", "grace@example.com"), "B-2")
    bad_a.record("deposit", 25)
    print("broken A:", bad_a.transactions)
    print("broken B:", bad_b.transactions)
    print("same list:", bad_a.transactions is bad_b.transactions)
    print("on the class:", BrokenAccount.transactions)

    ada.roles.append("admin")
    print("Ada.roles:", ada.roles)
    print("class roles:", User.roles)
    print("new user roles:", User.from_email("al@example.com").roles)


if __name__ == "__main__":
    main()
