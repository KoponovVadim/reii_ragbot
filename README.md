# RAG Train

RAG (Retrieval-Augmented Generation) приложение на FastAPI для ответов на вопросы с использованием источников.

## Описание

Приложение предоставляет REST API для:
- Задания вопросов и получения ответов с указанием источников
- Сохранения истории вопросов в БД
- Сохранённых вопросов по ID

## Структура проекта

```
.
├── main.py              # FastAPI приложение
├── database.py          # Конфигурация БД (SQLAlchemy + databases)
├── pydantic_train.py    # Pydantic модели для валидации
├── questions.py         # (опционально)
├── requirements.txt     # Зависимости проекта
├── .gitignore          # Git исключения
└── README.md           # Этот файл
```

## Требования

- Python 3.11+
- PostgreSQL (или другая БД, поддерживаемая SQLAlchemy)

## Зависимости

- **FastAPI** - веб-фреймворк
- **Uvicorn** - ASGI сервер
- **Pydantic** - валидация данных
- **SQLAlchemy** - ORM
- **databases** - асинхронная работа с БД
- **asyncpg** - драйвер PostgreSQL

## Установка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
```

2. Активируйте окружение:
```bash
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install fastapi uvicorn pydantic sqlalchemy databases[postgresql] asyncpg
```

## Конфигурация

Установите переменную окружения `DATABASE_URL` (по умолчанию используется PostgreSQL):
```bash
export DATABASE_URL="postgresql://user:password@localhost/dbname"
```

Или отредактируйте `database.py`:
```python
DATABASE_URL = "postgresql://user:password@localhost/dbname"
```

## Запуск

Запустите сервер Uvicorn:
```bash
uvicorn main:app --reload
```

Сервер будет доступен по адресу: `http://localhost:8000`

### API документация

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### POST /ask
Задание вопроса и получение ответа.

**Запрос:**
```json
{
  "text": "Какой ваш вопрос?"
}
```

**Ответ:**
```json
{
  "answer": "Вы спросили: 'Какой ваш вопрос?'. Но я пока ничего не знаю!",
  "sources": ["Источник 1", "Источник 2"],
  "confidence": 0.95
}
```

### POST /questions
Сохранение вопроса в БД.

**Запрос:**
```json
{
  "text": "Текст вопроса"
}
```

**Ответ:**
```json
{
  "id": 1,
  "text": "Текст вопроса",
  "created_at": "2026-02-24 10:30:45.123456"
}
```

### GET /questions?question_id=1
Получение сохранённого вопроса по ID.

**Ответ:**
```json
{
  "id": 1,
  "text": "Текст вопроса",
  "created_at": "2026-02-24 10:30:45.123456"
}
```

## Разработка

Для локальной разработки используйте SQLite вместо PostgreSQL:

```python
# database.py
DATABASE_URL = "sqlite:///./test.db"
```

## Лицензия

MIT
