# Лабораторная работа №2 — Git Flow

**Студент:** Зинин Павел, группа ИДБ-25-06  
**Дисциплина:** Промышленное программирование, МГТУ «СТАНКИН»  
**Репозиторий:** https://github.com/ZininPasha/laba2

Консольный калькулятор на Python. Демонстрирует Git Flow, PR/код-ревью, разрешение конфликтов, Git hooks.

## Структура для проверки

| Требование лабы | Где смотреть |
|-----------------|--------------|
| Отчёт (PDF) | `docs/ЛР2_Отчет.pdf` |
| Git Flow (ветки) | `main`, `develop`, `feature/*` |
| Код-ревью | `docs/CODE_REVIEW.md` |
| Конфликт | `docs/CONFLICT_RESOLUTION.md`, `docs/conflict_before.txt` |
| Hooks | `githooks/pre-commit`, `githooks/post-commit` |
| Лог коммитов | `commit.log` |

## Установка hooks (после клонирования)

```cmd
powershell -File scripts\install_hooks.ps1
pip install -r requirements-dev.txt
```

## Запуск

```cmd
py -3 -m src.main
```
