"""Episode 3 — properties and name mangling. Run: python temperature.py"""


class Temperature:
    def __init__(self, celsius: float) -> None:
        self._celsius = 0.0
        self.celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError(f"celsius below absolute zero: {value}")
        self._celsius = float(value)

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = (float(value) - 32) * 5 / 9

    def __repr__(self) -> str:
        return f"Temperature(celsius={self._celsius})"


class Ledger:
    def __init__(self) -> None:
        self._entries: list[str] = []
        self.__audit_key = "secret"

    def add(self, line: str) -> None:
        self._entries.append(line)

    def audit_key(self) -> str:
        return self.__audit_key


class SubLedger(Ledger):
    def __init__(self) -> None:
        super().__init__()
        self.__audit_key = "subclass-secret"


def main() -> None:
    room = Temperature(0.0)
    print("celsius:", room.celsius)
    print("fahrenheit:", room.fahrenheit)
    room.celsius = 100.0
    print("boiling F:", room.fahrenheit)
    room.fahrenheit = 32
    print("after 32 F:", room.celsius, room.fahrenheit)

    try:
        room.celsius = -300
    except ValueError as exc:
        print("rejected:", exc)

    led = Ledger()
    led.add("opened")
    print("public-by-convention _entries:", led._entries)
    print("mangled from outside:", led._Ledger__audit_key)
    print("hasattr __audit_key:", hasattr(led, "__audit_key"))

    sub = SubLedger()
    print("base key via method:", sub.audit_key())
    print("subclass mangled:", sub._SubLedger__audit_key)


if __name__ == "__main__":
    main()
