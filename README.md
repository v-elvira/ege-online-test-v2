# EGE API

FastAPI-приложение со слоистой структурой: конфигурация, API, БД, модели, схемы и сервисы.

## Требования

- Python 3.11+
- [uv](https://astral.sh) 0.5+
- PostgreSQL 14+

## Установка и запуск

```bash
uv sync
```

Dev (по умолчанию читается `.env.development`):

```bash
uv run uvicorn app.main:app --reload
```

Прод — скопируйте пример и заполните секреты:

```bash
copy .env.production.example .env.production
```

На Linux/macOS: `cp .env.production.example .env.production`.

```bash
set APP_ENV=production
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

На Linux/macOS: `APP_ENV=production uv run uvicorn app.main:app --host 0.0.0.0 --port 8000`.

Файл выбирается по `APP_ENV`: `development` / `dev` → `.env.development`, `production` / `prod` → `.env.production`. Переменные окружения процесса важнее значений из файла.

Приложение: [http://127.0.0.1:8000](http://127.0.0.1:8000).

- OpenAPI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Healthcheck: [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)

Проверка линтеров: 
`uv run ruff check .`

Проверка форматирования:
`uv run ruff format --check .`

## Переменные окружения

Основная БД — PostgreSQL через `asyncpg`.

Задайте `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB` — из них соберётся DSN. Либо укажите `DATABASE_URL` целиком (`postgresql+asyncpg://user:pass@host:5432/dbname`); обычный `postgresql://` будет приведён к `postgresql+asyncpg://`.

В production `DEBUG` должен быть `false`, `SECRET_KEY` — не дефолтный.

Создайте базу до запуска, например: `CREATE DATABASE ege;`.

## Структура

```
app/
  main.py          # точка входа, CORS
  core/            # settings (Pydantic), безопасность
  api/v1/          # эндпоинты
  db/              # SQLAlchemy engine и сессии
  models/          # ORM-модели
  schemas/         # Pydantic-схемы
  services/        # бизнес-логика
.env.development   # локальные настройки
.env.production    # прод (не в git)
```

### Активация Git-хуков (Ruff)
Для включения автоматической проверки кода перед коммитом:
```
uv sync
uv run pre-commit install --overwrite
```
(будет создан/пересоздан хук .git/hooks/pre-commit)


Для запуска проверки без коммита:
```
uv run pre-commit run --all-files
```
