import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.pipeline import ask

# Настройка логов (пишем и в файл, и в консоль)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(os.getenv("LOG_FILE", "logs/api.log")),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("api")

app = FastAPI(title="RAG Assistant API")

# Разрешаем запросы с клиента (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Схема запроса: ожидаем JSON вида {"question": "текст"}
class Question(BaseModel):
    question: str

# Проверка работоспособности сервера
@app.get("/health")
def health():
    return {"status": "ok"}

# Основной маршрут для вопросов
@app.post("/ask")
def ask_endpoint(payload: Question):
    log.info("QUESTION: %s", payload.question)
    result = ask(payload.question)
    log.info("ANSWER: %s", result["answer"][:200])
    
    # --- НОВЫЙ КОД: Убираем дубликаты страниц ---
    unique_sources = []
    seen = set()
    for src in result["sources"]:
        # Если такой страницы еще нет в списке, добавляем
        if src["page"] not in seen:
            unique_sources.append(src)
            seen.add(src["page"])
    result["sources"] = unique_sources
    # ---------------------------------------------
    
    return result