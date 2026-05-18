"""Точка входа: интерактивный калькулятор."""

from src.calculator import add, divide, multiply, subtract
from src.logger import get_logger

logger = get_logger("calculator")

OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def run() -> None:
    """Запуск простого REPL-калькулятора."""
    logger.info("Старт калькулятора")
    print("Калькулятор (лаб. №2). Операции: + - * /")
    print("Введите 'q' для выхода.")
    while True:
        op = input("Операция: ").strip()
        if op.lower() == "q":
            logger.info("Выход")
            break
        if op not in OPERATIONS:
            print("Неизвестная операция")
            continue
        try:
            a = float(input("a = "))
            b = float(input("b = "))
            result = OPERATIONS[op](a, b)
            logger.info("Операция %s: %s %s %s = %s", op, a, op, b, result)
            print(f"Результат: {result}")
        except ValueError as exc:
            print(f"Ошибка: {exc}")


if __name__ == "__main__":
    run()
