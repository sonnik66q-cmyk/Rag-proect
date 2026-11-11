from dotenv import load_dotenv
import os

load_dotenv()

GIGACHAT_CLIENT_ID = os.getenv("GIGACHAT_CLIENT_ID")
GIGACHAT_CLIENT_SECRET = os.getenv("GIGACHAT_CLIENT_SECRET")
GIGACHAT_MODEL = os.getenv("GIGACHAT_MODEL", "GigaChat")

if not GIGACHAT_CLIENT_ID or not GIGACHAT_CLIENT_SECRET:
    raise ValueError("Ключи GigaChat не найдены в .env")