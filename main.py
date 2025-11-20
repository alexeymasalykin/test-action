"""
Простое FastAPI приложение для получения текущего времени сервера
"""
from datetime import datetime
import pytz
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

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


class TimeConvertRequest(BaseModel):
    """Модель запроса для конвертации времени"""
    time: str = Field(..., description="Время в формате HH:MM или HH:MM:SS (UTC)")
    timezone: str = Field(..., description="Название часового пояса или города (например: Екатеринбург, Москва)")


class TimeConvertResponse(BaseModel):
    """Модель ответа с конвертированным временем"""
    original_time: str
    original_timezone: str
    converted_time: str
    converted_timezone: str
    timezone_offset: str


# Словарь для маппинга названий городов на часовые пояса
TIMEZONE_MAPPING = {
    # Российские города
    "москва": "Europe/Moscow",
    "екатеринбург": "Asia/Yekaterinburg",
    "санкт-петербург": "Europe/Moscow",
    "спб": "Europe/Moscow",
    "новосибирск": "Asia/Novosibirsk",
    "казань": "Europe/Moscow",
    "челябинск": "Asia/Yekaterinburg",
    "самара": "Europe/Samara",
    "омск": "Asia/Omsk",
    "красноярск": "Asia/Krasnoyarsk",
    "владивосток": "Asia/Vladivostok",
    "иркутск": "Asia/Irkutsk",
    "хабаровск": "Asia/Vladivostok",
    "якутск": "Asia/Yakutsk",
    "магадан": "Asia/Magadan",
    "камчатка": "Asia/Kamchatka",
    "калининград": "Europe/Kaliningrad",
    "мурманск": "Europe/Moscow",
    "ростов-на-дону": "Europe/Moscow",
    "нижний новгород": "Europe/Moscow",
    "уфа": "Asia/Yekaterinburg",
    "пермь": "Asia/Yekaterinburg",
    "краснодар": "Europe/Moscow",
    "воронеж": "Europe/Moscow",
    "саратов": "Europe/Saratov",
    "волгоград": "Europe/Volgograd",
    # Международные города
    "нью-йорк": "America/New_York",
    "лос-анджелес": "America/Los_Angeles",
    "чикаго": "America/Chicago",
    "лондон": "Europe/London",
    "париж": "Europe/Paris",
    "берлин": "Europe/Berlin",
    "токио": "Asia/Tokyo",
    "пекин": "Asia/Shanghai",
    "дубай": "Asia/Dubai",
    "сидней": "Australia/Sydney",
    "мельбурн": "Australia/Melbourne",
    "сингапур": "Asia/Singapore",
    "сеул": "Asia/Seoul",
    "бангкок": "Asia/Bangkok",
    "джакарта": "Asia/Jakarta",
    "манила": "Asia/Manila",
    "гонконг": "Asia/Hong_Kong",
    "тайбэй": "Asia/Taipei",
    "мumbai": "Asia/Kolkata",
    "дели": "Asia/Kolkata",
    "каир": "Africa/Cairo",
    "йоханнесбург": "Africa/Johannesburg",
    "рио-де-жанейро": "America/Sao_Paulo",
    "мехико": "America/Mexico_City",
    "буэнос-айрес": "America/Argentina/Buenos_Aires",
}


def get_timezone(city_name: str) -> pytz.BaseTzInfo:
    """
    Получает объект часового пояса по названию города или часового пояса
    
    Args:
        city_name: Название города или часового пояса
        
    Returns:
        Объект часового пояса pytz
        
    Raises:
        HTTPException: Если часовой пояс не найден
    """
    city_lower = city_name.lower().strip()
    
    # Проверяем маппинг городов
    if city_lower in TIMEZONE_MAPPING:
        timezone_str = TIMEZONE_MAPPING[city_lower]
    else:
        # Пробуем использовать название как есть (может быть стандартное название типа Asia/Yekaterinburg)
        timezone_str = city_name
    
    try:
        return pytz.timezone(timezone_str)
    except pytz.exceptions.UnknownTimeZoneError:
        raise HTTPException(
            status_code=400,
            detail=f"Часовой пояс '{city_name}' не найден. Используйте название города или стандартное название часового пояса (например: Asia/Yekaterinburg)"
        )


@app.get("/")
async def root():
    """Корневой эндпоинт с информацией об API"""
    return {
        "message": "Time Server API",
        "endpoints": {
            "/time": "GET - получить текущее время сервера",
            "/date": "GET - получить текущую дату сервера",
            "/date/formatted": "GET - получить дату в разных форматах",
            "/time/convert": "POST - конвертировать время между часовыми поясами"
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


@app.post("/time/convert", response_model=TimeConvertResponse)
async def convert_time(request: TimeConvertRequest):
    """
    Конвертирует время из UTC в указанный часовой пояс
    
    Args:
        request: Запрос с временем и часовым поясом
        
    Returns:
        TimeConvertResponse: Объект с конвертированным временем
        
    Raises:
        HTTPException: При ошибке парсинга времени или неверном часовом поясе
    """
    try:
        # Парсим время из строки
        time_parts = request.time.split(":")
        if len(time_parts) < 2:
            raise HTTPException(status_code=400, detail="Неверный формат времени. Используйте HH:MM или HH:MM:SS")
        
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        second = int(time_parts[2]) if len(time_parts) > 2 else 0
        
        if not (0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60):
            raise HTTPException(status_code=400, detail="Неверное значение времени")
        
        # Создаем datetime объект в UTC (используем сегодняшнюю дату)
        today = datetime.utcnow().date()
        utc_time = datetime.combine(today, datetime.min.time().replace(hour=hour, minute=minute, second=second))
        utc_time = pytz.UTC.localize(utc_time)
        
        # Получаем целевой часовой пояс
        target_tz = get_timezone(request.timezone)
        
        # Конвертируем время
        converted_time = utc_time.astimezone(target_tz)
        
        # Получаем смещение часового пояса
        offset = converted_time.strftime("%z")
        offset_formatted = f"UTC{offset[:3]}:{offset[3:]}" if offset else "UTC+0"
        
        return TimeConvertResponse(
            original_time=utc_time.strftime("%H:%M:%S"),
            original_timezone="UTC",
            converted_time=converted_time.strftime("%H:%M:%S"),
            converted_timezone=request.timezone,
            timezone_offset=offset_formatted
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Ошибка парсинга времени: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


@app.get("/health")
async def health_check():
    """Эндпоинт для проверки работоспособности сервера"""
    return {"status": "ok", "service": "time-server"}

