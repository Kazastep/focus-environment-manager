# Правила разработки

## Общий процесс

Для каждой задачи:

1. Взять Issue из GitHub Project.
2. Перевести задачу в статус `В работе`.
3. Рабочая ветка создаётся от актуальной dev.
4. Выполнить задачу.
5. Сделать понятные коммиты.
6. Отправить ветку на GitHub.
7. Создать Pull Request в dev и связать его с Issue.
8. После review выполнить Squash and merge в dev.

Работа с задачами подробнее описана здесь:

[Доска проекта](docs/project-board.md)

## Ветки

Одна задача = одна ветка.

Основные ветки:
- `main` — стабильная версия проекта.
- `dev` — основная ветка разработки.

Все рабочие ветки создаются от `dev`.
Прямые push в `main` и `dev` запрещены правилами команды.

Используем:

```text
feature/
fix/
docs/
refactor/
```

Желательно указать номер Issue:

```text
feature/AN-01-activity-metrics
fix/BE-03-session-history
docs/DB-02-schema-description
refactor/BE-01-backend-structure
```

## Коммиты

Сообщение должно коротко отвечать на вопрос: что изменилось?

```text
Добавить отслеживание активности
Исправить расчет состояния покоя
Обновить архитектуру
Удалить неиспользуемую модель
```

## Pull Request

Каждая задача попадает в `dev` через Pull Request.

Для рабочих задач:
- base: `dev`
- compare: рабочая ветка
- способ слияния: `Squash and merge`

После проверки изменений `dev` объединяется с `main`
через отдельный Pull Request:
- base: `main`
- compare: `dev`
- способ слияния: `Create a merge commit`

PR должен быть связан с Issue:

```text
Closes #12
```

## Обновление рабочей ветки

Перед началом новой задачи:

```bash
git switch dev
git pull origin dev
git switch -c feature/BE-04-example