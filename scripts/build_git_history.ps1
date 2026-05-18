# Автоматизация Git Flow для лабораторной №2
$ErrorActionPreference = "Stop"
$proj = (git rev-parse --show-toplevel)
Set-Location $proj

Copy-Item "$proj\githooks\pre-commit" "$proj\.git\hooks\pre-commit" -Force
Copy-Item "$proj\githooks\post-commit" "$proj\.git\hooks\post-commit" -Force

function Git-Commit {
    param([string]$Message)
    git add -A
    git commit -m $Message
}

# --- main: начальный проект ---
git checkout -B main 2>$null
git add .gitignore README.md requirements-dev.txt setup.cfg src scripts githooks docs
Git-Commit "chore: initial calculator project with gitignore and hooks"

# --- develop ---
git branch develop
git checkout develop

# --- feature/add-logging (3 коммита + исправления ревью) ---
git checkout -b feature/add-logging

@'
import logging

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
'@ | Set-Content -Encoding utf8 "$proj\src\logger.py"

git add src/logger.py
Git-Commit "feat: add logger module"

# main.py with logging (review issue: no log on ValueError)
@'
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
'@ | Set-Content -Encoding utf8 "$proj\src\main.py"

git add src/main.py
Git-Commit "feat: integrate logging in main REPL"

# Review fix 1: docstring
@'
import logging

def get_logger(name: str) -> logging.Logger:
    """Возвращает настроенный логгер с выводом в консоль.

    Args:
        name: имя логгера (обычно __name__ модуля).

    Returns:
        Экземпляр logging.Logger с уровнем INFO.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
'@ | Set-Content -Encoding utf8 "$proj\src\logger.py"

git add src/logger.py
Git-Commit "docs: add docstring to get_logger (code review)"

# Review fix 2: log ValueError
@'
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
            logger.warning("Некорректный ввод: %s", exc)
            print(f"Ошибка: {exc}")


if __name__ == "__main__":
    run()
'@ | Set-Content -Encoding utf8 "$proj\src\main.py"

git add src/main.py README.md
(Git-Commit "fix: log ValueError on invalid input (code review)")

git checkout develop
git merge --no-ff feature/add-logging -m "merge: feature/add-logging into develop (PR approved)"

# --- settings для конфликта ---
@'
"""Настройки приложения."""

APP_VERSION = "1.0.0"
TEAM = "core"
'@ | Set-Content -Encoding utf8 "$proj\src\settings.py"

git add src/settings.py
Git-Commit "chore: add settings module on develop"

# --- conflict branch A ---
git checkout -b feature/conflict-author-a
@'
"""Настройки приложения (команда Alpha)."""

APP_VERSION = "1.1.0-team-a"
TEAM = "alpha"
'@ | Set-Content -Encoding utf8 "$proj\src\settings.py"
git add src/settings.py
Git-Commit "feat(team-a): bump version and set team alpha"

# --- conflict branch B from develop ---
git checkout develop
git checkout -b feature/conflict-author-b
@'
"""Настройки приложения (команда Beta)."""

APP_VERSION = "1.1.0-team-b"
TEAM = "beta"
'@ | Set-Content -Encoding utf8 "$proj\src\settings.py"
git add src/settings.py
Git-Commit "feat(team-b): bump version and set team beta"

# Merge A first
git checkout develop
git merge --no-ff feature/conflict-author-a -m "merge: feature/conflict-author-a into develop"

# Merge B with conflict
git merge --no-ff feature/conflict-author-b -m "merge: feature/conflict-author-b (conflict)" 2>&1
# expect conflict - resolve manually below if needed

if (Test-Path "$proj\src\settings.py") {
    $content = @'
"""Настройки приложения (объединённая версия после конфликта)."""

APP_VERSION = "1.1.0"
TEAM = "combined"
'@
    Set-Content -Encoding utf8 "$proj\src\settings.py" $content
    git add src/settings.py
    if (git diff --cached --quiet) { } else {
        git commit -m "merge: resolve settings conflict (combined version)"
    }
}

# Release to main
git checkout main
git merge --no-ff develop -m "release: merge develop into main v1.1.0"

Write-Host "`n=== Git log (oneline) ==="
git log --oneline --graph --all -25
