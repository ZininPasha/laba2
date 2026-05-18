#!/usr/bin/env python3
"""Pre-commit: проверка стиля изменённых Python-файлов через flake8."""

import subprocess
import sys


def staged_python_files() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [f for f in result.stdout.splitlines() if f.endswith(".py")]


def main() -> int:
    files = staged_python_files()
    if not files:
        return 0
    print("pre-commit: flake8 для", ", ".join(files))
    proc = subprocess.run(
        [sys.executable, "-m", "flake8", *files],
        cwd=subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip(),
    )
    if proc.returncode != 0:
        print("pre-commit: проверка стиля не пройдена. Коммит отменён.")
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
