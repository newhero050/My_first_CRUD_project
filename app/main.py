from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import category, products, auth, permission, reviews

app = FastAPI()

# Разрешаем браузеру делать запросы к нашему API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Разрешить запросы откуда угодно (для разработки)
    allow_credentials=True,
    allow_methods=["*"],       # Разрешить все HTTP-методы (GET, POST, DELETE и т.д.)
    allow_headers=["*"],       # Разрешить все заголовки (включая Authorization)
)

@app.get('/')
async def welcome() -> dict:
    return {"message": "My e-commerce app"}

app.include_router(category.router)
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(permission.router)
app.include_router(reviews.router)