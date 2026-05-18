# Документация по разрешению конфликта

## Ситуация

Два «разработчика» создали ветки от `develop` и изменили один файл `src/settings.py`:

| Ветка | Изменение `APP_VERSION` | Дополнительно |
|-------|-------------------------|---------------|
| `feature/conflict-author-a` | `"1.1.0-team-a"` | `TEAM = "alpha"` |
| `feature/conflict-author-b` | `"1.1.0-team-b"` | `TEAM = "beta"` |

Ветка **author-a** была слита в `develop` через merge.  
При слиянии **author-b** возник конфликт в `src/settings.py`.

## Команды

```bash
git checkout develop
git merge feature/conflict-author-b
# CONFLICT in src/settings.py

git status
git mergetool
# или ручное редактирование файла

git add src/settings.py
git commit -m "merge: разрешён конфликт settings (объединены версии команд)"
```

## Стратегия

Выбрана **объединяющая стратегия**: итоговая версия `1.1.0`, команда указана как `combined`, чтобы сохранить смысл обеих веток без потери метаданных.

## Итоговое содержимое (фрагмент)

```python
APP_VERSION = "1.1.0"
TEAM = "combined"
```

## Маркеры конфликта (до разрешения)

```
<<<<<<< HEAD
APP_VERSION = "1.1.0-team-a"
TEAM = "alpha"
=======
APP_VERSION = "1.1.0-team-b"
TEAM = "beta"
>>>>>>> feature/conflict-author-b
```
