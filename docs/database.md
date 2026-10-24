# База данных

В проекте используется **PostgreSQL 16** для хранения пользователей, рабочих сессий, событий активности и статистики.

Для локальной разработки PostgreSQL запускается через Docker Compose. Backend взаимодействует с базой данных через SQLAlchemy.

## 1. Используемые технологии

- PostgreSQL 16 — реляционная база данных.
- Docker Compose — запуск PostgreSQL в контейнере.
- SQLAlchemy Core — описание таблиц и выполнение SQL-запросов.
- asyncpg — асинхронный драйвер PostgreSQL.
- psycopg — синхронный драйвер PostgreSQL (используется для учебных проверок).
- Pydantic Settings — загрузка конфигурации из переменных окружения.

## 2. Настройка окружения

Перед запуском необходимо создать `.env` в корне проекта на основе `.env.example`.

Пример переменных:

```dotenv
POSTGRES_USER=focus_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=focus_db
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5440
```

Значения пользователя, пароля и базы должны соответствовать настройкам PostgreSQL в `compose.yaml`.

**Важно:** файл `.env` не должен попадать в Git.

## 3. Запуск PostgreSQL

Из корневой директории проекта:

```bash
docker compose up -d
```

Проверка состояния:

```bash
docker compose ps
```

Просмотр логов:

```bash
docker compose logs db
```

Остановка контейнеров:

```bash
docker compose stop
```

Удаление контейнеров без удаления именованных томов:

```bash
docker compose down
```

Не используйте `docker compose down -v`, если необходимо сохранить данные PostgreSQL.

## 4. Подключение к PostgreSQL

При запуске Python непосредственно на компьютере:

```text
HOST=127.0.0.1
PORT=5440
```

При запуске backend внутри того же Docker Compose (если соответствующий сервис настроен):

```text
HOST=db
PORT=5432
```

`db` — имя сервиса PostgreSQL в Compose.

Внутри Docker Compose контейнеры обращаются друг к другу через внутреннюю сеть Docker.

## 5. Структура файлов

```text
database/
├── config.py        # Настройки подключения
├── database.py      # Engine и фабрика сессий
├── models.py        # Описание таблиц
├── core.py          # Создание таблиц
└── test_insert.py   # Учебная проверка INSERT
```

## 6. Создание таблиц

Перед запуском необходимо установить зависимости Python и запустить PostgreSQL.

Из корневой директории проекта:

```bash
python -m database.core
```

SQLAlchemy создаст отсутствующие таблицы на основе описаний из `models.py`.

Таблицы:

- `users` — пользователи.
- `sessions` — рабочие сессии.
- `events` — события активности.
- `statistics` — дневная статистика пользователей.

**Важно:** `create_all()` создаёт отсутствующие таблицы, но не обновляет структуру существующих. Для изменения схемы в дальнейшем планируется использовать Alembic.

## 7. Проверка через DBeaver

Настройки подключения:

```text
Host: localhost
Port: 5440
Database: focus_db
Username: значение POSTGRES_USER
Password: значение POSTGRES_PASSWORD
```

После подключения таблицы находятся в:

`Schemas → public → Tables`

Необходимо убедиться, что существуют `users`, `sessions`, `events`, `statistics`.

## 8. Работа с данными

Для асинхронного взаимодействия с PostgreSQL используется `AsyncSession`, создаваемая через `async_sessionmaker`.

Учебный INSERT был успешно выполнен и проверен через DBeaver.

CRUD-операции для FastAPI будут реализованы в отдельных задачах backend.

## 9. Сохранность данных

Данные PostgreSQL должны храниться в постоянном томе Docker.

При использовании именованного тома данные сохраняются после:

- `docker compose stop`
- `docker compose down`
- `docker compose up -d`

Команда `docker compose down -v` удаляет тома, управляемые Compose, и может привести к потере данных.

Перед использованием необходимо проверить фактическую конфигурацию `volumes` в `compose.yaml`.