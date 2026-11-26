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
    # Обрезаем ответ для лога, чтобы не раздувать файл
    log.info("ANSWER: %s", result["answer"][:200])
    return result