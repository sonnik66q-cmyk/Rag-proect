import os
import urllib3
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

def ask_gigachat(messages: list, mock_mode=False) -> str:
    if mock_mode:
        return "[MOCK-ОТВЕТ]: Это тестовый ответ без подключения к сети."

    key = os.getenv("GIGACHAT_CREDENTIALS") or os.getenv("GIGACHAT_CLIENT_SECRET")
    if not key:
        return "Ошибка: Ключ не найден в файле .env"

    try:
        # 1. Преобразуем список словарей в список объектов Messages
        giga_messages = []
        for msg in messages:
            role = msg["role"]
            if role == "system":
                giga_messages.append(Messages(role=MessagesRole.SYSTEM, content=msg["content"]))
            elif role == "user":
                giga_messages.append(Messages(role=MessagesRole.USER, content=msg["content"]))
            elif role == "assistant":
                giga_messages.append(Messages(role=MessagesRole.ASSISTANT, content=msg["content"]))

        # 2. Создаем объект Chat (обертку для запроса)
        chat_request = Chat(messages=giga_messages)

        with GigaChat(credentials=key, verify_ssl_certs=False, model="GigaChat-2") as client:
            # 3. Отправляем объект Chat
            response = client.chat(chat_request)
            
            # 4. Извлекаем текст ответа (структура ответа тоже изменилась)
            return response.choices[0].message.content
            
    except Exception as e:
        return f"Ошибка при обращении к GigaChat: {e}"