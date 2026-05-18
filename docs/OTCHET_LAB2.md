# ОТЧЁТ ПО ЛАБОРАТОРНОЙ РАБОТЕ №2

**Дисциплина:** Промышленное программирование  
**Тема:** Организация промышленного workflow с Git  
**Университет:** МГТУ «СТАНКИН»

---

## Титульный лист

| | |
|---|---|
| **ФИО** | _Заполните: Фамилия И.О._ |
| **Группа** | _Заполните_ |
| **Вариант** | Индивидуальный (свой проект) |
| **Проект** | Калькулятор (`lab2-git-workflow`) |
| **Дата** | 18.05.2026 |

---

## 1. Цель работы

Закрепить навыки промышленной работы с Git: модель Git Flow, pull request и код-ревью, разрешение конфликтов, автоматизация через Git hooks (pre-commit / post-commit).

---

## 2. Описание проекта

Учебное Python-приложение — консольный калькулятор с модулями:

- `src/calculator.py` — операции
- `src/main.py` — REPL-интерфейс
- `src/logger.py` — логирование (feature-ветка)
- `src/settings.py` — настройки (конфликт веток)

Путь к репозиторию: `C:\Users\<пользователь>\Documents\lab2-git-workflow`

---

## 3. Организация репозитория

| Шаг | Выполнено |
|-----|-----------|
| `git init` | Да |
| Ветки `main`, `develop` | Да |
| `.gitignore` (Python, IDE, venv, кэш) | Да |
| Удалённый репозиторий | Инструкция: `docs/GITHUB_SETUP.md` |

---

## 4. Git Flow

### 4.1. Ветки

- **main** — стабильная версия (релиз 1.1.0)
- **develop** — интеграционная ветка разработки
- **feature/add-logging** — новая функциональность (логирование)
- **feature/conflict-author-a**, **feature/conflict-author-b** — имитация параллельной работы

### 4.2. История коммитов

```
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

Полный лог: `git log --oneline --graph --all`

---

## 5. Pull Request и код-ревью

**PR:** `feature/add-logging` → `develop`

**Описание изменений:** добавлен модуль логирования, интеграция в `main.py`.

### Замечания ревью (≥2) и исправления

| № | Замечание | Исправление | Коммит |
|---|-----------|-------------|--------|
| 1 | Нет docstring у `get_logger` | Добавлен docstring | `c9aaeb1` |
| 2 | Не логируется `ValueError` при неверном вводе | `logger.warning(...)` | `ddc3df1` |

Подробности: `docs/CODE_REVIEW.md`

**Скриншот для отчёта:** страница Pull Request на GitHub с комментариями (после `git push`).

---

## 6. Конфликт и разрешение

### 6.1. Сценарий

1. От `develop` созданы две ветки, изменён один файл `src/settings.py`.
2. `feature/conflict-author-a` слита в `develop` первой.
3. При слиянии `feature/conflict-author-b` — **конфликт**.

### 6.2. Маркеры конфликта (фрагмент)

См. файл `docs/conflict_before.txt`:

```
<<<<<<< HEAD
APP_VERSION = "1.1.0-team-a"
TEAM = "alpha"
=======
APP_VERSION = "1.1.0-team-b"
TEAM = "beta"
>>>>>>> feature/conflict-author-b
```

### 6.3. Команды

```bash
git checkout develop
git merge feature/conflict-author-a    # успешно
git merge feature/conflict-author-b    # CONFLICT
git status
git mergetool                          # vscode / vimdiff / вручную
git add src/settings.py
git commit -m "merge: resolve settings conflict"
```

### 6.4. Стратегия

Объединение: `APP_VERSION = "1.1.0"`, `TEAM = "combined"`.

### 6.5. Скриншоты для отчёта

- `git status` с unmerged paths
- Окно `git mergetool` или редактор с маркерами конфликта
- Итоговый `src/settings.py` после разрешения

Подробнее: `docs/CONFLICT_RESOLUTION.md`

---

## 7. Git hooks

### 7.1. pre-commit

Проверяет staged-файлы `src/*.py` через **flake8**. При ошибке коммит отменяется.

**Листинг** (копия в репозитории: `githooks/pre-commit`):

```sh
#!/bin/sh
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

**Демонстрация отказа:** файл с `x=1` → flake8 `E225` → коммит не создан.

### 7.2. post-commit

Записывает в `commit.log`: время, хеш, автор, сообщение.

**Листинг** (`githooks/post-commit`):

```sh
#!/bin/sh
set -e
ROOT="$(git rev-parse --show-toplevel)"
if command -v py >/dev/null 2>&1; then
  exec py -3 "$ROOT/scripts/post_commit_log.py"
...
fi
```

### 7.3. commit.log (фрагмент)

```
[2026-05-18 10:56:48 UTC] 553a4b3... | Zinin Pavel <...> | feat: add logger module
[2026-05-18 10:57:07 UTC] ddc3df1... | Zinin Pavel <...> | fix: log ValueError on invalid input (code review)
[2026-05-18 10:58:27 UTC] 782f67c... | Zinin Pavel <...> | merge: resolve settings conflict ...
```

**Скриншот:** содержимое `commit.log` в проводнике или терминале после нескольких коммитов.

---

## 8. Вывод

В ходе работы настроен репозиторий с моделью **Git Flow**, выполнена разработка в feature-ветке с осмысленными коммитами, имитировано **код-ревью** с исправлением замечаний, разрешён **merge-конфликт** в `src/settings.py`, настроены **pre-commit** (flake8) и **post-commit** (лог `commit.log`). Получены практические навыки, соответствующие компетенциям ПК-3.1 и ПК-3.2.

---

## Приложение: экспорт в PDF

1. Откройте этот файл в Word / Typora / VS Code.
2. Заполните ФИО и группу на титульном листе.
3. Добавьте скриншоты (PR, конфликт, commit.log).
4. Сохраните как **PDF**.
