"""Episode 1 — dict+functions vs a class. Run: python bank_account.py"""


def make_account(
    owner: str, balance: float = 0.0, ledger: list | None = None
) -> dict:
    if ledger is None:
        ledger = []
    return {"owner": owner, "balance": balance, "ledger": ledger}


def deposit(account: dict, amount: float) -> None:
    account["balance"] += amount
    account["ledger"].append(("deposit", amount))


def withdraw(account: dict, amount: float) -> None:
    if amount > account["balance"]:
        raise ValueError("insufficient funds")
    account["balance"] -= amount
    account["ledger"].append(("withdraw", amount))


def make_account_broken(
    owner: str, balance: float = 0.0, ledger: list = []
) -> dict:
    return {"owner": owner, "balance": balance, "ledger": ledger}


class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner = owner
        self.balance = balance
        self.ledger: list[tuple[str, float]] = []

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.ledger.append(("deposit", amount))

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
        self.ledger.append(("withdraw", amount))

    def __repr__(self) -> str:
        return f"BankAccount(owner={self.owner!r}, balance={self.balance})"


def main() -> None:
    ada = {"owner": "Ada", "balance": 100.0}
    grace = {"owner": "Ada", "balance": 100.0}
    print("same values, different objects:", ada == grace, ada is grace)

    a = make_account_broken("Ada", 100)
    b = make_account_broken("Grace", 50)
    deposit(a, 25)
    print("broken — Ada ledger:", a["ledger"])
    print("broken — Grace ledger:", b["ledger"])
    print("same list object:", a["ledger"] is b["ledger"])

    c = make_account("Ada", 100)
    d = make_account("Grace", 50)
    deposit(c, 25)
    print("fixed dict — Grace ledger:", d["ledger"])

    acct = BankAccount("Ada", 100)
    acct.deposit(25)
    other = BankAccount("Grace", 50)
    print("class — Ada:", acct)
    print("class — Grace ledger:", other.ledger)
    print("identity:", acct is other, "equality by default:", acct == other)


if __name__ == "__main__":
    main()
