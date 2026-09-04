# EGE API

FastAPI-приложение со слоистой структурой: конфигурация, API, БД, модели, схемы и сервисы.

## Требования

- Python 3.11+

## Установка и запуск

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

На Linux/macOS активация окружения: `source .venv/bin/activate`.

Приложение будет доступно по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

- Документация OpenAPI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Healthcheck: [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)

## Переменные окружения

Скопируйте значения из `.env` и при необходимости измените `SECRET_KEY` и `DATABASE_URL`. По умолчанию используется асинхронный SQLite (`sqlite+aiosqlite:///./app.db`). Для PostgreSQL: `postgresql+asyncpg://user:pass@host:5432/dbname` (добавьте `asyncpg` в зависимости).

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
```
