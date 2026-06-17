import math
from dataclasses import dataclass, field
from typing import Protocol


class HasArea(Protocol):
    def area(self) -> float: ...


@dataclass
class Shape:
    color: str = "red"

    def area(self) -> float:
        raise NotImplementedError

    def describe(self) -> str:
        return f"{self.color} {type(self).__name__} - area: {self.area():.4f}"


@dataclass
class Circle(Shape):
    radius: float = 0.0

    @property
    def diameter(self) -> float:
        return self.radius * 2

    def area(self) -> float:
        return math.pi * self.radius ** 2


@dataclass
class Rectangle(Shape):
    width: float = 0.0
    height: float = 0.0

    def area(self) -> float:
        return self.width * self.height


@dataclass
class Triangle(Shape):
    base: float = 0.0
    height: float = 0.0

    def area(self) -> float:
        return 0.5 * self.base * self.height


@dataclass(frozen=True)
class Config:
    host: str
    port: int = 8080
    tags: list[str] = field(default_factory=list)


def total_area(shapes: list[HasArea]) -> float:
    return sum(s.area() for s in shapes)


def main() -> None:
    shapes: list[Shape] = [
        Circle(color="blue", radius=5.0),
        Rectangle(color="green", width=4.0, height=3.0),
        Triangle(color="purple", base=6.0, height=4.0),
    ]

    for s in shapes:
        print(s.describe())

    print(f"\nTotal area: {total_area(shapes):.4f}")  # type: ignore[arg-type]

    # Dataclass features
    c1 = Circle(color="red", radius=3.0)
    c2 = Circle(color="red", radius=3.0)
    print(f"\nc1 == c2: {c1 == c2}")
    print(f"c1 is c2: {c1 is c2}")
    print(f"diameter: {c1.diameter}")

    # Frozen dataclass
    cfg = Config(host="localhost", tags=["web", "api"])
    print(f"\nConfig: {cfg}")
    try:
        cfg.port = 9000  # type: ignore[misc]
    except Exception as e:
        print(f"Immutable: {e}")


if __name__ == "__main__":
    main()
