"""
Простое FastAPI приложение для получения текущего времени сервера
"""
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

# Создаем экземпляр приложения FastAPI
app = FastAPI(
    title="Time Server API",
    description="Простое API для получения текущего времени сервера",
    version="1.0.0"
)


class TimeResponse(BaseModel):
    """Модель ответа с текущим временем"""
    current_time: str
    timestamp: float
    timezone: str = "UTC"


class DateResponse(BaseModel):
    """Модель ответа с текущей датой"""
    current_date: str
    date_iso: str
    day_of_week: str
    day_of_year: int
    week_number: int
    timezone: str = "UTC"


@app.get("/")
async def root():
    """Корневой эндпоинт с информацией об API"""
    return {
        "message": "Time Server API",
        "endpoints": {
            "/time": "GET - получить текущее время сервера",
            "/date": "GET - получить текущую дату сервера",
            "/date/formatted": "GET - получить дату в разных форматах"
        }
    }


@app.get("/time", response_model=TimeResponse)
async def get_current_time():
    """
    Возвращает текущее время сервера
    
    Returns:
        TimeResponse: Объект с текущим временем, timestamp и timezone
    """
    now = datetime.utcnow()
    return TimeResponse(
        current_time=now.strftime("%Y-%m-%d %H:%M:%S"),
        timestamp=now.timestamp(),
        timezone="UTC"
    )


@app.get("/date", response_model=DateResponse)
async def get_current_date():
    """
    Возвращает текущую дату сервера
    
    Returns:
        DateResponse: Объект с текущей датой, днем недели и другой информацией
    """
    now = datetime.utcnow()
    # Получаем номер недели в году
    week_number = now.isocalendar()[1]
    
    # Названия дней недели на русском
    days_of_week = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье"
    }
    
    return DateResponse(
        current_date=now.strftime("%d.%m.%Y"),
        date_iso=now.strftime("%Y-%m-%d"),
        day_of_week=days_of_week[now.weekday()],
        day_of_year=now.timetuple().tm_yday,
        week_number=week_number,
        timezone="UTC"
    )


@app.get("/date/formatted")
async def get_formatted_date():
    """
    Возвращает текущую дату в различных форматах
    
    Returns:
        dict: Словарь с датой в разных форматах
    """
    now = datetime.utcnow()
    
    return {
        "iso_format": now.strftime("%Y-%m-%d"),
        "russian_format": now.strftime("%d.%m.%Y"),
        "us_format": now.strftime("%m/%d/%Y"),
        "full_format": now.strftime("%d %B %Y"),
        "short_format": now.strftime("%d.%m.%y"),
        "timestamp": now.timestamp(),
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "timezone": "UTC"
    }


@app.get("/health")
async def health_check():
    """Эндпоинт для проверки работоспособности сервера"""
    return {"status": "ok", "service": "time-server"}

