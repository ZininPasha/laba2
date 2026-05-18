# ОТЧЁТ ПО ЛАБОРАТОРНОЙ РАБОТЕ №2

**Дисциплина:** Промышленное программирование  
**Тема:** Организация промышленного workflow с Git  
**Университет:** МГТУ «СТАНКИН»

---

## Титульный лист

| | |
|---|---|
| **ФИО** | Зинин Павел |
| **Группа** | ИДБ-25-06 |
| **Проект** | Калькулятор (консольное Python-приложение) |
| **Репозиторий** | https://github.com/ZininPasha/laba2 |
| **Дата** | 18.05.2026 |

---

## 1. Цель работы

Закрепить навыки промышленной работы с Git: модель Git Flow, pull request и код-ревью, разрешение конфликтов, автоматизация через Git hooks (pre-commit / post-commit).

---

## 2. Описание проекта

Учебное Python-приложение — консольный калькулятор:

- `src/calculator.py` — арифметические операции
- `src/main.py` — REPL-интерфейс
- `src/logger.py` — логирование (ветка `feature/add-logging`)
- `src/settings.py` — настройки (имитация конфликта веток)

---

## 3. Организация репозитория

| Требование | Выполнено |
|------------|-----------|
| Локальный репозиторий | Да |
| Удалённый репозиторий | https://github.com/ZininPasha/laba2 |
| `git remote add origin` | Настроен |
| `.gitignore` (Python, IDE, venv, сборка) | Файл `.gitignore` в корне |

---

## 4. Git Flow

### 4.1. Ветки

| Ветка | Назначение |
|-------|------------|
| `main` | Стабильные версии (релиз 1.1.0) |
| `develop` | Интеграционная ветка разработки |
| `feature/add-logging` | Новая функциональность — логирование |
| `feature/conflict-author-a` | Параллельные изменения (команда A) |
| `feature/conflict-author-b` | Параллельные изменения (команда B) |

### 4.2. История коммитов

```
* 714d51f docs: add lab report, GitHub setup and conflict example
* cf2631b chore: add commit.log from post-commit hook
*   d28f904 release: merge develop into main v1.1.0
|\  
| *   782f67c merge: resolve settings conflict (combined version after mergetool)
| |\  
| | * 0f2e696 feat(team-b): bump version and set team beta
| * |   d848ba6 merge: feature/conflict-author-a into develop
| |\ \  
| | * 84878fb feat(team-a): bump version and set team alpha
| * ce0e2c0 chore: fix hooks and add settings module on develop
| * fb8f7bc merge: feature/add-logging into develop (PR approved)
| * ddc3df1 fix: log ValueError on invalid input (code review)
| * c9aaeb1 docs: add docstring to get_logger (code review)
| * 94b5982 feat: integrate logging in main REPL
| * 553a4b3 feat: add logger module
* c1f08e7 chore: initial calculator project with gitignore and hooks
```

Команда просмотра: `git log --oneline --graph --all`

---

## 5. Pull Request и код-ревью

**PR:** `feature/add-logging` → `develop`  
**Репозиторий:** https://github.com/ZininPasha/laba2/pulls

**Описание изменений:** добавлен модуль `src/logger.py`, логирование операций в `src/main.py`.

### Замечания ревью (≥2) и исправления

| № | Замечание ревьюера | Исправление | Коммит |
|---|-------------------|-------------|--------|
| 1 | Нет docstring у `get_logger` | Добавлен docstring с описанием параметров | `c9aaeb1` |
| 2 | Не логируется `ValueError` при неверном вводе | Добавлен `logger.warning(...)` | `ddc3df1` |

Подробное описание: `docs/CODE_REVIEW.md`

---

## 6. Конфликт и разрешение

### 6.1. Сценарий

1. От `develop` созданы ветки `feature/conflict-author-a` и `feature/conflict-author-b`.
2. Обе изменили `src/settings.py`.
3. Ветка **author-a** слита в `develop` первой (через merge).
4. При слиянии **author-b** возник конфликт.

### 6.2. Маркеры конфликта

Файл `docs/conflict_before.txt`:

```
<<<<<<< HEAD
APP_VERSION = "1.1.0-team-a"
TEAM = "alpha"
=======
APP_VERSION = "1.1.0-team-b"
TEAM = "beta"
>>>>>>> feature/conflict-author-b
```

### 6.3. Использованные команды

```bash
git checkout develop
git merge feature/conflict-author-a
git merge feature/conflict-author-b
git status
git mergetool
git add src/settings.py
git commit -m "merge: resolve settings conflict (combined version after mergetool)"
```

### 6.4. Стратегия разрешения

Объединение изменений обеих веток: `APP_VERSION = "1.1.0"`, `TEAM = "combined"`.

Итоговый файл `src/settings.py` в ветке `develop`.

Подробнее: `docs/CONFLICT_RESOLUTION.md`

---

## 7. Git hooks

После клонирования hooks устанавливаются командой: `powershell -File scripts\install_hooks.ps1`

### 7.1. pre-commit

Проверяет staged-файлы `src/*.py` через **flake8**. При ошибке коммит отменяется.

**Файл:** `githooks/pre-commit` (копия в `.git/hooks/pre-commit`)

```sh
#!/bin/sh
# Pre-commit hook: проверка стиля (flake8) для staged .py файлов
set -e
ROOT="$(git rev-parse --show-toplevel)"
if command -v py >/dev/null 2>&1; then
  exec py -3 "$ROOT/scripts/pre_commit_check.py"
elif command -v python3 >/dev/null 2>&1; then
  exec python3 "$ROOT/scripts/pre_commit_check.py"
else
  exec python "$ROOT/scripts/pre_commit_check.py"
fi
```

**Проверка:** коммит файла с нарушением стиля (`x=1` без пробелов) отклоняется с ошибкой flake8 `E225`.

### 7.2. post-commit

**Файл:** `githooks/post-commit` (копия в `.git/hooks/post-commit`)

```sh
#!/bin/sh
# Post-commit hook: логирование коммита в commit.log
set -e
ROOT="$(git rev-parse --show-toplevel)"
if command -v py >/dev/null 2>&1; then
  exec py -3 "$ROOT/scripts/post_commit_log.py"
elif command -v python3 >/dev/null 2>&1; then
  exec python3 "$ROOT/scripts/post_commit_log.py"
else
  exec python "$ROOT/scripts/post_commit_log.py"
fi
```

### 7.3. Лог коммитов (commit.log)

```
[2026-05-18 13:56:20 UTC] c1f08e78905c1ed3281260558677703cef409094 | Zinin Pavel <pashazerfa@gmail.com> | chore: initial calculator project with gitignore and hooks
[2026-05-18 10:56:48 UTC] 553a4b34aadadb5dfec28297c4c43ab5e81e8ab3 | Zinin Pavel <pashazerfa@gmail.com> | feat: add logger module
[2026-05-18 10:56:49 UTC] 94b59821725885765b69790512104553755a2549 | Zinin Pavel <pashazerfa@gmail.com> | feat: integrate logging in main REPL
[2026-05-18 10:57:06 UTC] c9aaeb158fd1c24b3257c45a93ca40417a33576e | Zinin Pavel <pashazerfa@gmail.com> | docs: add docstring to get_logger (code review)
[2026-05-18 10:57:07 UTC] ddc3df113db6db1762c4d113067ded3868a45c7b | Zinin Pavel <pashazerfa@gmail.com> | fix: log ValueError on invalid input (code review)
[2026-05-18 10:57:23 UTC] ce0e2c02f5906af65cd6af2443f56ad1243d4021 | Zinin Pavel <pashazerfa@gmail.com> | chore: fix hooks and add settings module on develop
[2026-05-18 10:57:35 UTC] 84878fb4dc2ca06e3c3e5d76664ea4facd3933cf | Zinin Pavel <pashazerfa@gmail.com> | feat(team-a): bump version and set team alpha
[2026-05-18 10:57:44 UTC] 0f2e6961b7d3b5a0bffca49070716d7977d80d71 | Zinin Pavel <pashazerfa@gmail.com> | feat(team-b): bump version and set team beta
[2026-05-18 10:58:27 UTC] 782f67c873f8b00e02ffd76b5ca151294d7977f6 | Zinin Pavel <pashazerfa@gmail.com> | merge: resolve settings conflict (combined version after mergetool)
[2026-05-18 10:58:28 UTC] cf2631b4c06c1216f5f8967a89b79ab445cb3644 | Zinin Pavel <pashazerfa@gmail.com> | chore: add commit.log from post-commit hook
[2026-05-18 10:59:30 UTC] 714d51f06bfc55244dbbff00755504733f3fd8a1 | Zinin Pavel <pashazerfa@gmail.com> | docs: add lab report, GitHub setup and conflict example
```

---

## 8. Вывод

Выполнена организация Git-репозитория по модели **Git Flow** с ветками `main`, `develop` и `feature/*`. Разработана функциональность в отдельной feature-ветке с осмысленными коммитами, проведено **код-ревью** с исправлением двух замечаний. Имитирована командная работа: создан и разрешён **merge-конфликт** в `src/settings.py`. Настроены **pre-commit** (flake8) и **post-commit** (логирование в `commit.log`). Репозиторий опубликован на GitHub.
