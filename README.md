# SHORTURL

Сервис сокращения ссылок (аналог bit.ly), построенный на **FastAPI** и **PostgreSQL**.

---

## Требования

- Docker
- Docker Compose

---

## Быстрый старт

1. **Клонировать репозиторий:**

```bash
git clone <repo-url>
cd shorturl
```

2. **Создать файл окружения:**

```bash
cp .env.example .env
```

*Отредактируйте `.env`, указав свои данные для БД.*

3. **Запустить проект:**

```bash
docker compose up -d
```

*При запуске сервис `fastapi` автоматически применит все существующие миграции к базе данных.*

---

## 📖 Использование API

После запуска сервис доступен по адресу: `http://localhost:8000`

* **Интерактивная документация (Swagger): http://localhost:8000/docs
* **Альтернативная документация (ReDoc): http://localhost:8000/redoc

---

## 👨‍💻 Разработка и миграции

В проекте используется **Alembic**. Все файлы миграций (`alembic/versions`) хранятся в Git.

### Создание новой миграции:

Если вы изменили модели в `src/`, создайте файл миграции:

```bash
docker compose --profile tools run --rm migrate alembic revision --autogenerate -m "Ваше описание изменений"

```

### Применение миграций:

Миграции применяются автоматически при старте основного контейнера. Чтобы применить их вручную без перезапуска API:

```bash
docker compose exec fastapi alembic upgrade head

```

---

## 🧪 Тестирование

В папке `tests/` находится файл `test_main.http` и `pytest` тесты для сервиса.
