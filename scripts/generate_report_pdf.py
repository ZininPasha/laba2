#!/usr/bin/env python3
"""Генерация PDF-отчёта по ЛР2 в формате МГТУ СТАНКИН."""

from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "LR2_Otchet.pdf"
FONT = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_MONO = Path(r"C:\Windows\Fonts\consola.ttf")


class LabReport(FPDF):
  def __init__(self):
    super().__init__()
    self.add_font("Arial", "", str(FONT))
    self.add_font("Arial", "B", str(FONT_BOLD))
    self.add_font("Consolas", "", str(FONT_MONO))
    self.set_auto_page_break(auto=True, margin=20)
    self.toc_entries: list[tuple[str, int]] = []

  def footer(self):
    self.set_y(-15)
    self.set_font("Arial", "", 9)
    self.cell(0, 8, "Лабораторная работа № 2", align="L")
    self.cell(0, 8, str(self.page_no()), align="R")

  def section_title(self, num: str, title: str):
    self.set_x(self.l_margin)
    self.set_font("Arial", "B", 14)
    self.multi_cell(self.epw, 8, f"{num} {title}")
    self.ln(2)

  def body(self, text: str):
    self.set_x(self.l_margin)
    self.set_font("Arial", "", 12)
    self.multi_cell(self.epw, 6, text)
    self.ln(2)

  def code_block(self, text: str, size: int = 8):
    self.set_x(self.l_margin)
    self.set_font("Consolas", "", size)
    self.set_fill_color(245, 245, 245)
    for line in text.strip().splitlines():
      self.multi_cell(self.epw, 4.5, "  " + line, fill=True)
    self.ln(2)

  def bullet(self, text: str):
    self.set_x(self.l_margin)
    self.set_font("Arial", "", 12)
    self.multi_cell(self.epw, 6, f"    - {text}")


def title_page(pdf: LabReport):
  pdf.add_page()
  pdf.set_font("Arial", "", 12)
  pdf.ln(25)
  pdf.multi_cell(
    0,
    7,
    "Федеральное государственное автономное образовательное учреждение "
    "высшего образования\n"
    "«Московский государственный технологический университет «СТАНКИН»\n"
    "(ФГАОУ ВО «МГТУ «СТАНКИН»)\n"
    "Кафедра «Информационных технологий и вычислительных систем»",
    align="C",
  )
  pdf.ln(20)
  pdf.set_font("Arial", "B", 16)
  pdf.multi_cell(
    0,
    9,
    "ЛАБОРАТОРНАЯ РАБОТА №2\n"
    "«Организация промышленного workflow с Git»",
    align="C",
  )
  pdf.ln(8)
  pdf.set_font("Arial", "", 14)
  pdf.multi_cell(0, 8, "по дисциплине «Промышленное программирование»", align="C")
  pdf.ln(30)
  pdf.set_font("Arial", "", 14)
  pdf.cell(0, 8, "Выполнил: студент гр. ИДБ-25-06", ln=True, align="R")
  pdf.cell(0, 8, "Зинин П.А.", ln=True, align="R")
  pdf.ln(8)
  pdf.cell(0, 8, "Проверил: Старший преподаватель", ln=True, align="R")
  pdf.cell(0, 8, "Мельников В.П.", ln=True, align="R")
  pdf.ln(30)
  pdf.cell(0, 8, "Москва, 2026 г.", ln=True, align="C")


def toc_page(pdf: LabReport):
  pdf.add_page()
  pdf.set_font("Arial", "B", 14)
  pdf.cell(0, 10, "ОГЛАВЛЕНИЕ", ln=True, align="C")
  pdf.ln(5)
  pdf.set_font("Arial", "", 12)
  items = [
    ("1", "Цель работы", 3),
    ("2", "Теоретическая основа", 3),
    ("3", "Организация репозитория", 4),
    ("4", "Реализация Git Flow", 4),
    ("5", "Pull Request и код-ревью", 5),
    ("6", "Разрешение конфликта", 6),
    ("7", "Настройка Git hooks", 7),
    ("8", "Логирование коммитов", 8),
    ("9", "ВЫВОДЫ", 9),
  ]
  for num, title, page in items:
    dots = "." * max(1, 55 - len(title) - len(num))
    pdf.cell(0, 7, f"{num} {title} {dots} {page}", ln=True)


def build_report():
  pdf = LabReport()
  title_page(pdf)
  toc_page(pdf)

  pdf.add_page()
  pdf.section_title("1", "Цель работы")
  pdf.body(
    "Закрепить на практике навыки использования промышленных практик работы "
    "с системами контроля версий: моделей ветвления, процедур код-ревью, "
    "разрешения конфликтов и автоматизации с помощью Git hooks."
  )

  pdf.section_title("2", "Теоретическая основа")
  pdf.body("Перед выполнением работы изучены следующие темы:")
  pdf.bullet("Задача контроля версий. Обзор существующих решений.")
  pdf.bullet("Локальная работа с Git.")
  pdf.bullet("Работа с удалённым Git-репозиторием (GitHub).")

  pdf.section_title("3", "Организация репозитория")
  pdf.body(
    "Разработан учебный проект — консольный калькулятор на Python. "
    "Репозиторий опубликован на GitHub: https://github.com/ZininPasha/laba2"
  )
  pdf.body("Выполнены следующие шаги:")
  pdf.bullet("Инициализирован локальный репозиторий.")
  pdf.bullet("Создан удалённый репозиторий и настроен remote origin.")
  pdf.bullet("Настроен файл .gitignore (Python, IDE, venv, кэш сборки).")
  pdf.body("Структура проекта:")
  pdf.code_block(
    """lab2-git-workflow/
├── .gitignore
├── README.md
├── commit.log
├── githooks/
│   ├── pre-commit
│   └── post-commit
├── scripts/
│   ├── pre_commit_check.py
│   └── post_commit_log.py
└── src/
    ├── calculator.py
    ├── main.py
    ├── logger.py
    └── settings.py"""
  )

  pdf.section_title("4", "Реализация Git Flow")
  pdf.body("Созданы основные ветки:")
  pdf.bullet("main — стабильные версии (релиз 1.1.0);")
  pdf.bullet("develop — ветка разработки;")
  pdf.bullet("feature/add-logging — новая функциональность (логирование);")
  pdf.bullet("feature/conflict-author-a, feature/conflict-author-b — имитация командной работы.")
  pdf.body("История коммитов (git log --oneline --graph --all):")
  pdf.code_block(
    """* ad09d4e chore: prepare repo for submission
* cf2631b chore: add commit.log from post-commit hook
*   d28f904 release: merge develop into main v1.1.0
|\\  
| *   782f67c merge: resolve settings conflict
| | * 0f2e696 feat(team-b): bump version
| * |   d848ba6 merge: feature/conflict-author-a
| | * 84878fb feat(team-a): bump version
| * fb8f7bc merge: feature/add-logging (PR approved)
| * ddc3df1 fix: log ValueError (code review)
| * c9aaeb1 docs: add docstring (code review)
| * 553a4b3 feat: add logger module
* c1f08e7 chore: initial project""",
    size=7,
  )

  pdf.add_page()
  pdf.section_title("5", "Pull Request и код-ревью")
  pdf.body(
    "Создана ветка feature/add-logging от develop. Выполнено 4 осмысленных "
    "коммита. Ветка отправлена на GitHub. Создан Pull Request на слияние "
    "feature/add-logging в develop."
  )
  pdf.body("Замечания ревьюера и исправления:")
  pdf.set_font("Arial", "", 11)
  pdf.cell(10, 7, "№", border=1)
  pdf.cell(70, 7, "Замечание", border=1)
  pdf.cell(55, 7, "Исправление", border=1)
  pdf.cell(25, 7, "Коммит", border=1, ln=True)
  rows = [
    ("1", "Нет docstring у get_logger", "Добавлен docstring", "c9aaeb1"),
    ("2", "Не логируется ValueError", "logger.warning(...)", "ddc3df1"),
  ]
  for row in rows:
    pdf.cell(10, 7, row[0], border=1)
    pdf.cell(70, 7, row[1], border=1)
    pdf.cell(55, 7, row[2], border=1)
    pdf.cell(25, 7, row[3], border=1, ln=True)
  pdf.ln(3)
  pdf.body("После исправления замечаний PR одобрен и слит в develop.")

  pdf.section_title("6", "Разрешение конфликта")
  pdf.body(
    "Два разработчика изменили файл src/settings.py в разных ветках от develop. "
    "Ветка feature/conflict-author-a слита в develop первой. При слиянии "
    "feature/conflict-author-b возник конфликт."
  )
  pdf.body("Маркеры конфликта:")
  pdf.code_block(
    """<<<<<<< HEAD
APP_VERSION = "1.1.0-team-a"
TEAM = "alpha"
=======
APP_VERSION = "1.1.0-team-b"
TEAM = "beta"
>>>>>>> feature/conflict-author-b"""
  )
  pdf.body("Использованные команды:")
  pdf.code_block(
    """git checkout develop
git merge feature/conflict-author-a
git merge feature/conflict-author-b
git status
git mergetool
git add src/settings.py
git commit -m "merge: resolve settings conflict\""""
  )
  pdf.body(
    "Стратегия: объединение изменений обеих веток. "
    "Итог: APP_VERSION = \"1.1.0\", TEAM = \"combined\"."
  )

  pdf.add_page()
  pdf.section_title("7", "Настройка Git hooks")
  pdf.body("7.1 Pre-commit hook (проверка стиля flake8)")
  pdf.body("Файл githooks/pre-commit:")
  pdf.code_block(
    Path(ROOT / "githooks" / "pre-commit").read_text(encoding="utf-8"),
    size=7,
  )
  pdf.body(
    "При нарушении стиля (например, E225 — отсутствие пробелов вокруг оператора) "
    "коммит отменяется."
  )
  pdf.body("7.2 Post-commit hook (логирование)")
  pdf.body("Файл githooks/post-commit:")
  pdf.code_block(
    Path(ROOT / "githooks" / "post-commit").read_text(encoding="utf-8"),
    size=7,
  )

  pdf.section_title("8", "Логирование коммитов")
  pdf.body("Post-commit hook записывает данные в файл commit.log:")
  log_text = Path(ROOT / "commit.log").read_text(encoding="utf-8")
  pdf.code_block(log_text[:1200] + ("..." if len(log_text) > 1200 else ""), size=6)

  pdf.section_title("9", "ВЫВОДЫ")
  pdf.body(
    "В ходе выполнения лабораторной работы были приобретены и закреплены "
    "следующие навыки:"
  )
  pdf.bullet("Организация репозитория по модели Git Flow (main, develop, feature/*).")
  pdf.bullet("Разработка функциональности в feature-ветке с осмысленными коммитами.")
  pdf.bullet("Проведение код-ревью с исправлением замечаний в Pull Request.")
  pdf.bullet("Разрешение merge-конфликта с использованием git mergetool.")
  pdf.bullet("Настройка pre-commit (flake8) и post-commit (лог commit.log) hooks.")
  pdf.bullet("Публикация проекта на GitHub: https://github.com/ZininPasha/laba2")

  OUT.parent.mkdir(parents=True, exist_ok=True)
  pdf.output(str(OUT))
  print(f"PDF saved: {OUT}")


if __name__ == "__main__":
  build_report()
