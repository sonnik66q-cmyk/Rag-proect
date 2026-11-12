import os
import urllib3
from dotenv import load_dotenv
from gigachat import GigaChat

# Отключаем предупреждения SSL для локальной разработки
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

def ask_gigachat(messages: list, mock_mode=False) -> str:
    """Отправляет сообщение в GigaChat и возвращает текст ответа."""
    
    # Режим-заглушка для тестов без интернета
    if mock_mode:
        return "[MOCK-ОТВЕТ]: Это тестовый ответ без подключения к сети."

    # Ищем ключ в переменных окружения (поддерживаем оба названия)
    key = os.getenv("GIGACHAT_CREDENTIALS") or os.getenv("GIGACHAT_CLIENT_SECRET")
    
    # Если ключа нет вообще
    if not key:
        return "❌ Ошибка: Ключ не найден в файле .env. Пожалуйста, добавьте GIGACHAT_CREDENTIALS."

    try:
        # Подключаемся к GigaChat (модель GigaChat-2)
        with GigaChat(credentials=key, verify_ssl_certs=False, model="GigaChat-2") as client:
            # Отправляем сообщения и получаем ответ
            response = client.chat(messages)
            # Возвращаем текст ответа
            return response.choices[0].message.content
            
    except Exception as e:
        # Превращаем объект ошибки в строку для анализа
        error_text = str(e)
        
        # Проверяем, что именно пошло не так
        if "401" in error_text or "403" in error_text:
            return "❌ Ошибка авторизации: Неверный ключ доступа. Проверьте GIGACHAT_CREDENTIALS в файле .env"
        elif "400" in error_text:
            return "❌ Ошибка формата ключа: Ключ поврежден или имеет неверный формат (Base64). Скопируйте Authorization Key из личного кабинета Сбера заново."
        elif "timeout" in error_text.lower() or "connection" in error_text.lower():
            return "❌ Ошибка сети: Не удалось связаться с сервером GigaChat. Проверьте интернет."
        else:
            # Если ошибка неизвестная, выводим её краткую версию (до первого двоеточия)
            short_error = error_text.split(":")[0] 
            return f"❌ Неизвестная ошибка: {short_error}"