from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = "<h1>Главная страница</h1><p>Добро пожаловать!</p>"
    return html_content