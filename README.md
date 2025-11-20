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
    "/time": "GET - получить текущее время сервера",
    "/date": "GET - получить текущую дату сервера",
    "/date/formatted": "GET - получить дату в разных форматах"
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

### GET `/date`
Возвращает текущую дату сервера с дополнительной информацией.

**Ответ:**
```json
{
  "current_date": "15.01.2024",
  "date_iso": "2024-01-15",
  "day_of_week": "Понедельник",
  "day_of_year": 15,
  "week_number": 3,
  "timezone": "UTC"
}
```

### GET `/date/formatted`
Возвращает текущую дату в различных форматах.

**Ответ:**
```json
{
  "iso_format": "2024-01-15",
  "russian_format": "15.01.2024",
  "us_format": "01/15/2024",
  "full_format": "15 January 2024",
  "short_format": "15.01.24",
  "timestamp": 1705327845.123456,
  "year": 2024,
  "month": 1,
  "day": 15,
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

## CI/CD с GitHub Actions

Проект включает автоматизированный деплой через GitHub Actions. При пуше в ветку `main` или `master` автоматически:
1. Собирается Docker образ
2. Образ публикуется в GitHub Container Registry (ghcr.io)
3. Выполняется деплой на удаленный сервер через SSH

### Настройка секретов в GitHub

Для работы CI/CD необходимо настроить следующие секреты в настройках репозитория (`Settings` → `Secrets and variables` → `Actions`):

- **`SSH_HOST`** - IP адрес или доменное имя удаленного сервера
- **`SSH_USER`** - имя пользователя для SSH подключения
- **`SSH_PRIVATE_KEY`** - приватный SSH ключ для подключения к серверу
- **`SSH_PORT`** (опционально) - порт SSH (по умолчанию 22)

### Настройка SSH ключа на сервере

1. Сгенерируйте SSH ключ (если еще нет):
```bash
ssh-keygen -t ed25519 -C "github-actions"
```

2. Добавьте публичный ключ на сервер:
```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@your-server
```

3. Скопируйте приватный ключ и добавьте его в секрет `SSH_PRIVATE_KEY`:
```bash
cat ~/.ssh/id_ed25519
```

### Настройка Docker на сервере

На удаленном сервере должен быть установлен Docker и настроен доступ к GitHub Container Registry:

```bash
# Логин в GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

### Ручной запуск workflow

Workflow можно запустить вручную через вкладку `Actions` в репозитории GitHub.

## Структура проекта

```
action-fastapi/
├── main.py                      # Основное приложение FastAPI
├── requirements.txt             # Зависимости проекта
├── Dockerfile                   # Docker конфигурация для сборки образа
├── .dockerignore                # Игнорируемые файлы для Docker
├── .env.example                 # Пример файла переменных окружения
├── .gitignore                   # Игнорируемые файлы для Git
├── .github/
│   └── workflows/
│       └── deploy.yml           # GitHub Actions workflow для CI/CD
└── README.md                    # Документация проекта
```

