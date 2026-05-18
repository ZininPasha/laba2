# Имитация код-ревью (feature/add-logging → develop)

## Pull Request: «Добавить модуль логирования»

**Ветка:** `feature/add-logging` → `develop`

### Описание изменений

- Добавлен модуль `src/logger.py` с функцией `get_logger`.
- В `src/main.py` подключено логирование операций калькулятора.
- Обновлён `README.md`.

### Замечания ревьюера (≥2)

1. **Стиль:** в `logger.py` отсутствует docstring у функции `get_logger` — добавить описание параметров.
2. **Обработка ошибок:** в `main.py` при неверном вводе числа нужно логировать предупреждение, а не только печатать в консоль.

### Исправления (коммиты в той же ветке)

- `docs: add docstring to get_logger`
- `fix: log ValueError on invalid numeric input`

### Статус

Замечания исправлены, PR одобрен и слит в `develop`.
