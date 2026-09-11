import uuid
from loguru import logger

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import v1_routers, v2_routers
from time import perf_counter, process_time

app = FastAPI()

# Разрешаем браузеру делать запросы к нашему API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Разрешить запросы откуда угодно (для разработки)
    allow_credentials=True,
    allow_methods=["*"],       # Разрешить все HTTP-методы (GET, POST, DELETE и т.д.)
    allow_headers=["*"],       # Разрешить все заголовки (включая Authorization)
)

logger.add('logs/app.log', rotation='5 MB', level='INFO', retention="5 days", compression='zip')
logger.add('logs/errors.log', level='ERROR', rotation='5 MB', retention="5 days", compression='zip')

@app.middleware("http")
async def my_middleware(request: Request, call_next):
    time = perf_counter()
    try:
        response = await call_next(request)
    except Exception as e:
        logger.exception(e)
        raise e
    time_process = perf_counter() - time
    request_uuid = str(uuid.uuid4())
    request_method = request.method
    request_path = request.url.path
    response.headers['X-Process-Time'] = f"{time_process:.4f}s"
    response.headers['X-Request-ID'] = request_uuid
    logger.info(f'Request URL: {request_path}, Request method: {request_method}, '
          f'Response status-code: {response.status_code}, Response time: {time_process:.4f}s, '
          f'Request UUID: {request_uuid}')

    return response

@app.get('/')
async def welcome() -> dict:
    return {"message": "My e-commerce app"}

app.include_router(v1_routers)
app.include_router(v2_routers)