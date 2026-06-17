import itertools
from dataclasses import dataclass


@dataclass
class Employee:
    name: str
    department: str
    salary: float
    years: int


EMPLOYEES = [
    Employee("Alice",  "Engineering", 95_000, 5),
    Employee("Bob",    "HR",          65_000, 3),
    Employee("Carol",  "Engineering", 105_000, 8),
    Employee("Dave",   "HR",          72_000, 6),
    Employee("Eve",    "Engineering", 88_000, 2),
    Employee("Frank",  "Sales",       78_000, 4),
    Employee("Grace",  "Sales",       82_000, 7),
]


def top_earners(employees: list[Employee], n: int = 3) -> list[Employee]:
    return sorted(employees, key=lambda e: e.salary, reverse=True)[:n]


def avg_salary_by_dept(employees: list[Employee]) -> dict[str, float]:
    by_dept = sorted(employees, key=lambda e: e.department)
    result: dict[str, float] = {}
    for dept, group in itertools.groupby(by_dept, key=lambda e: e.department):
        members = list(group)
        result[dept] = sum(e.salary for e in members) / len(members)
    return result


def main() -> None:
    # List comprehension — names of Engineering staff
    eng_names = [e.name for e in EMPLOYEES if e.department == "Engineering"]
    print(f"Engineering: {eng_names}")

    # Dict comprehension — name → salary map
    salary_map = {e.name: e.salary for e in EMPLOYEES}
    print(f"\nSalary map:")
    for name, sal in salary_map.items():
        print(f"  {name}: ${sal:,.0f}")

    # Generator — total salary spend (no intermediate list)
    total = sum(e.salary for e in EMPLOYEES)
    print(f"\nTotal salary spend: ${total:,.0f}")

    # Top earners
    print("\nTop 3 earners:")
    for e in top_earners(EMPLOYEES):
        print(f"  {e.name} ({e.department}): ${e.salary:,.0f}")

    # Average salary by department
    print("\nAverage salary by department:")
    for dept, avg in avg_salary_by_dept(EMPLOYEES).items():
        print(f"  {dept}: ${avg:,.0f}")

    # Senior employees (5+ years)
    seniors = [e.name for e in EMPLOYEES if e.years >= 5]
    print(f"\nSenior employees (5+ years): {seniors}")

    # Set — unique departments
    departments: set[str] = {e.department for e in EMPLOYEES}
    print(f"\nDepartments: {sorted(departments)}")

    # zip — pair names and years
    print("\nName -> years pairs:")
    for name, years in zip(
        [e.name for e in EMPLOYEES],
        [e.years for e in EMPLOYEES],
    ):
        print(f"  {name}: {years} yr(s)")

    # all / any
    print(f"\nAll earn > 60k: {all(e.salary > 60_000 for e in EMPLOYEES)}")
    print(f"Any earn > 100k: {any(e.salary > 100_000 for e in EMPLOYEES)}")


if __name__ == "__main__":
    main()
