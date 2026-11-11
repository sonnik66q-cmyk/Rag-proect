from gigachat import GigaChat
from src.config import GIGACHAT_CLIENT_ID, GIGACHAT_CLIENT_SECRET, GIGACHAT_MODEL

def generate_answer(question: str, hits: list[dict]) -> str:
    context = "\n\n".join(f"[стр. {h['page']}] {h['text']}" for h in hits)
    prompt = f"""Ты отвечаешь ТОЛЬКО по предоставленному контексту.
Если ответа в контексте нет — напиши: «В документе нет ответа».
Не выдумывай факты. В конце укажи страницы, откуда взята информация.

Контекст:
{context}

Вопрос: {question}"""

    giga = GigaChat(
        credentials=GIGACHAT_CLIENT_SECRET, 
        verify_ssl_certs=False,
        model=GIGACHAT_MODEL
    )
    response = giga.chat(prompt)
    return response.choices[0].message.content