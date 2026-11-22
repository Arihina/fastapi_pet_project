# Pet project on FastAPI.
## Topic

Учёт движения товара на оптовом складе: FastAPI + SQLAlchemy (async) + PostgreSQL,
серверный рендеринг Jinja2 + `app/static/script.js`.

## Запуск из консоли

Единственный поддерживаемый способ — запуск из **корня проекта** (там, где `app/`
и `.env`), чтобы `app.*` был импортируемым пакетом.

```bash
# 1. Зависимости (uv; создаёт .venv)
UV_CACHE_DIR="$PWD/.uv-cache" uv venv --python 3.12 .venv
UV_CACHE_DIR="$PWD/.uv-cache" uv pip install --python .venv/bin/python -r requirements.txt

# 2. Конфигурация
cp .env.example .env   # и вписать свои значения

# 3. Запуск (любой из вариантов)
.venv/bin/uvicorn app.main:app --reload          # канонический
.venv/bin/python -m app.main                     # то же самое
```

Приложение: <http://127.0.0.1:8000>, документация: <http://127.0.0.1:8000/docs>.
