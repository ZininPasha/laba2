# Публикация на GitHub / GitLab

Репозиторий подготовлен локально. Для связи с удалённым репозиторием:

## GitHub

1. Создайте репозиторий на https://github.com/new (например, `lab2-git-workflow`).
2. Выполните в папке проекта:

```powershell
cd $env:USERPROFILE\Documents\lab2-git-workflow
git remote add origin https://github.com/<ВАШ_ЛОГИН>/lab2-git-workflow.git
git push -u origin main
git push origin develop
git push origin feature/add-logging
git push origin feature/conflict-author-a
git push origin feature/conflict-author-b
```

3. На GitHub создайте **Pull Request**: `feature/add-logging` → `develop`.
4. Добавьте 2+ комментария ревью (см. `docs/CODE_REVIEW.md`) — они уже отражены в коммитах исправлений.
5. Второй PR `feature/conflict-author-b` → `develop` покажет конфликт, если первым слить `feature/conflict-author-a` без разрешения на GitHub (локально конфликт уже разрешён).

## Pull Request (шаблон описания)

**Заголовок:** feat: add logging module

**Описание:**
- Добавлен `src/logger.py`
- Логирование операций в `src/main.py`
- Исправлены замечания ревью (docstring, логирование ValueError)
