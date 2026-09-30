"""Episode 4 — inheritance, super, MRO. Run: python notifications.py"""


class Notification:
    def __init__(self, recipient: str) -> None:
        self.recipient = recipient
        self.sent = False

    def send(self, body: str) -> str:
        raise NotImplementedError("use a subclass")

    def mark_sent(self) -> None:
        self.sent = True

    def __repr__(self) -> str:
        return f"{type(self).__name__}(recipient={self.recipient!r}, sent={self.sent})"


class Email(Notification):
    def __init__(self, recipient: str, sender: str) -> None:
        super().__init__(recipient)
        self.sender = sender

    def send(self, body: str) -> str:
        line = f"email from {self.sender} to {self.recipient}: {body}"
        self.mark_sent()
        return line


class SMS(Notification):
    def __init__(self, recipient: str, gateway: str) -> None:
        super().__init__(recipient)
        self.gateway = gateway

    def send(self, body: str) -> str:
        line = f"sms via {self.gateway} to {self.recipient}: {body}"
        self.mark_sent()
        return line


class Logged:
    def send(self, body: str) -> str:
        result = super().send(body)  # type: ignore[misc]
        print(f"LOG: {result}")
        return result


class LoggedEmail(Logged, Email):
    pass


def dispatch(note: Notification, body: str) -> str:
    return note.send(body)


def main() -> None:
    email = Email("ada@example.com", sender="noreply@app.test")
    sms = SMS("+15550100", gateway="twilio")
    print(dispatch(email, "welcome"))
    print(dispatch(sms, "otp 123456"))
    print("email is Notification:", isinstance(email, Notification))
    print("type is Notification:", type(email) is Notification)
    print("MRO LoggedEmail:", [c.__name__ for c in LoggedEmail.__mro__])

    logged = LoggedEmail("ada@example.com", sender="noreply@app.test")
    dispatch(logged, "welcome")

    try:
        Notification("x").send("nope")
    except NotImplementedError as exc:
        print("base send:", exc)


if __name__ == "__main__":
    main()
