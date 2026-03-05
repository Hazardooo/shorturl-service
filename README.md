# 🔗 SHORTURL

Сервис сокращения ссылок (аналог bit.ly), построенный на современных технологиях. Позволяет мгновенно создавать короткие идентификаторы для длинных URL с отслеживанием статистики переходов.

---

## 🛠 Требования

* **Docker** и **Docker Compose**
* **Git**

---

## 🚀 Быстрый старт

1. **Клонировать репозиторий:**
```bash
git clone https://github.com/Hazardooo/shorturl-service.git
cd shorturl
```


2. **Настроить переменные окружения:**
```bash
cp .env.example .env
```


*Отредактируйте `.env`, указав свои настройки (БД, порты).*
3. **Запустить сервис:**
```bash
docker compose up -d
```


*При старте контейнер `fastapi` автоматически выполнит `alembic upgrade head` для подготовки базы данных.*

---

## 📖 Документация API

После запуска API доступно по адресу `http://localhost:8000`.

* **Swagger UI (Интерактивно):** http://localhost:8000/docs — лучший выбор для тестирования.
* **ReDoc (Справочник):** http://localhost:8000/redoc — удобное чтение схемы.

---

## 💻 Примеры использования

### 1. Создание короткой ссылки

Отправьте POST запрос с длинным URL. В ответ придет уникальный `short_id`.

**Запрос в Swagger:**
<img width="1410" height="547" alt="изображение" src="https://github.com/user-attachments/assets/a03159c3-9e7f-47d7-bd48-72e45bf10505" />


**Пример ответа:**

```json
{
  "original_url": "https://site.yummyani.me/",
  "short_id": "Kp6Vj5"
}

```

### 2. Переход (Redirect)

Подставьте полученный `short_id` в адресную строку браузера:
`http://localhost:8000/Kp6Vj5`
<img width="1456" height="84" alt="изображение" src="https://github.com/user-attachments/assets/7b5c4a52-d1d3-45e0-96d3-285e4f242235" />

> **Примечание:** Swagger не выполняет редирект в интерфейсе, поэтому используйте браузер или `curl -L`.

### 3. Статистика переходов

Узнайте, сколько раз была использована ваша ссылка:
`GET /stats/{short_id}`
<img width="1413" height="490" alt="изображение" src="https://github.com/user-attachments/assets/017e87f0-ee68-43a0-a01a-c8add9f79223" />

**Пример ответа:**

```json
{
  "clicks": 5
}

```

---

## ⚙️ Миграции (Alembic)

Проект использует систему миграций для управления схемой базы данных. Все версии хранятся в папке `alembic/versions`.

* **Создать новую миграцию (после изменения моделей):**
```bash
docker compose --profile tools run --rm migrate alembic revision --autogenerate -m "Add new field"

```


* **Применить миграции вручную:**
```bash
docker compose exec fastapi alembic upgrade head

```

---

## 🧪 Тестирование

### Автоматические тесты (Pytest)

Запуск тестов внутри Docker-контейнера:

```bash
docker compose exec -e PYTHONPATH=. fastapi pytest
```

### Ручные тесты (.http файл)

Для ручных тестов доступен файл `tests/test_main.http`.

---
