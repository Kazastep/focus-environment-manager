# Development Guide

## Workflow

Для каждой задачи:

1. Обновить `main`.
2. Создать отдельную ветку.
3. Выполнить задачу.
4. Сделать commit.
5. Отправить ветку на GitHub.
6. Создать Pull Request.
7. После review — merge в `main`.

## Branches

Используем формат:

```text
feature/name
fix/name
docs/name
refactor/name

Пример:
feature/session-api
feature/activity-tracker
fix/idle-calculation
docs/architecture
```

## Commits

Используем формат:

```text
Добавить эндпоинт для создания сессии
Исправить расчет времени простоя
Обновить архитектуру проекта
Удалить неиспользуемую модель активности
```

## Main branch

В `main` напрямую не работаем.

Любые изменения делаются в отдельной ветке и попадают в `main` через Pull Request.

## Tasks

Одна ветка должна соответствовать одной задаче.

Не стоит смешивать в одной ветке несколько несвязанных изменений.