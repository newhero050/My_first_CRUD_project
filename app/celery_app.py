from gc import enable

from celery import Celery
from app.config import settings
import time

celery = Celery("ecommerce_tasks",
                broker=settings.REDIS_URL,
                backend=settings.REDIS_URL)

celery.conf.update(timezone="Europe/Moscow",
                   enable_utc=True,
                   broker_connection_retry_on_startup=True)

@celery.task(name="simulate_heavy_report")
def simulate_heavy_report(report_name: str, seconds: int = 5):
    """Имитация очень тяжелой фоновой работы"""
    print(f"🔥 Воркер взял задачу: генерация отчета '{report_name}'...")
    time.sleep(seconds)
    print(f"✅ Отчет '{report_name}' готов!")
    return f"Отчет '{report_name}' успешно сформирован за {seconds} сек."