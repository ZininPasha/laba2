"""Простой калькулятор для демонстрации Git Flow."""


def add(a: float, b: float) -> float:
    """Сложение двух чисел."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Вычитание."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Умножение."""
    return a * b


def divide(a: float, b: float) -> float:
    """Деление с проверкой делителя."""
    if b == 0:
        raise ValueError("Деление на ноль недопустимо")
    return a / b
