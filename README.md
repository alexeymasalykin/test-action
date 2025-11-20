# Time Server API

Простое FastAPI приложение, возвращающее текущее время сервера.

## Установка

### 1. Создание виртуального окружения

```bash
python -m venv venv
```

### 2. Активация виртуального окружения

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения (опционально)

Скопируйте `.env.example` в `.env` и при необходимости измените настройки:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

## Запуск

### Запуск сервера разработки

```bash
uvicorn main:app --reload
```

Сервер будет доступен по адресу: `http://localhost:8000`

### Запуск с указанием хоста и порта

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Запуск с Docker

### Сборка образа

```bash
docker build -t time-server-api .
```

### Запуск контейнера

```bash
docker run -d -p 8000:8000 --name time-server time-server-api
```

Сервер будет доступен по адресу: `http://localhost:8000`

### Остановка контейнера

```bash
docker stop time-server
docker rm time-server
```

## API Эндпоинты

### GET `/`
Корневой эндпоинт с информацией об API.

**Ответ:**
```json
{
  "message": "Time Server API",
  "endpoints": {
    "/time": "GET - получить текущее время сервера"
  }
}
```

### GET `/time`
Возвращает текущее время сервера в формате UTC.

**Ответ:**
```json
{
  "current_time": "2024-01-15 14:30:45",
  "timestamp": 1705327845.123456,
  "timezone": "UTC"
}
```

### GET `/health`
Проверка работоспособности сервера.

**Ответ:**
```json
{
  "status": "ok",
  "service": "time-server"
}
```

## Документация API

После запуска сервера доступна автоматическая интерактивная документация:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Технологии

- **FastAPI** - современный веб-фреймворк для Python
- **Pydantic** - валидация данных
- **Uvicorn** - ASGI сервер

## Структура проекта

```
action-fastapi/
├── main.py              # Основное приложение FastAPI
├── requirements.txt     # Зависимости проекта
├── Dockerfile           # Docker конфигурация для сборки образа
├── .dockerignore        # Игнорируемые файлы для Docker
├── .env.example         # Пример файла переменных окружения
├── .gitignore          # Игнорируемые файлы для Git
└── README.md           # Документация проекта
```

