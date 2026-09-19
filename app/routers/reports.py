from fastapi import APIRouter
from app.celery_app import simulate_heavy_report, celery
from celery.result import AsyncResult

router = APIRouter(prefix='/reports', tags=['reports'])

@router.post('/start')
async def request_report(report_name: str):
    task = simulate_heavy_report.delay(report_name=report_name, seconds=20)
    return {"task_id": task.id, "status": "Задача отправлена в очередь"}

@router.get('/status/{task_id}')
async def get_status_report(task_id: str):
    res = AsyncResult(task_id, app=celery)
    return {
        "task_id": task_id,
        "status": res.status,
        "result": res.result if res.ready() else "Отчёт ещё формируется..."
    }


