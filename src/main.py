"""Точка входа: интерактивный калькулятор."""

from src.calculator import add, divide, multiply, subtract

OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def run() -> None:
    """Запуск простого REPL-калькулятора."""
    print("Калькулятор (лаб. №2). Операции: + - * /")
    print("Введите 'q' для выхода.")
    while True:
        op = input("Операция: ").strip()
        if op.lower() == "q":
            break
        if op not in OPERATIONS:
            print("Неизвестная операция")
            continue
        try:
            a = float(input("a = "))
            b = float(input("b = "))
            result = OPERATIONS[op](a, b)
            print(f"Результат: {result}")
        except ValueError as exc:
            print(f"Ошибка: {exc}")


if __name__ == "__main__":
    run()
