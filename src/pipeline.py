from src.pdf_loader import load_pages
from src.chunker import chunk_text
from src.embedder import embed
from src.vector_store import add_chunks, search
from src.llm import generate_answer

def ingest(file_path: str):
    print("1. Читаем файл...")
    pages = load_pages(file_path)
    
    print("2. Нарезаем на чанки...")
    all_chunks = []
    for p in pages:
        for i, chunk in enumerate(chunk_text(p["text"])):
            all_chunks.append({
                "text": chunk,
                "page": p["page"],
                "source": file_path.split("/")[-1].split("\\")[-1], 
                "chunk_id": i,
            })
            
    print(f"   Получено {len(all_chunks)} чанков.")
    print("3. Создаем эмбеддинги (это может занять время)...")
    vectors = embed([c["text"] for c in all_chunks])
    
    print("4. Сохраняем в базу данных...")
    add_chunks(all_chunks, vectors)
    
    print(f"УСПЕХ! Файл {file_path} проиндексирован.")


# --- НОВЫЙ КОД, КОТОРЫЙ МЫ ДОБАВЛЯЕМ ---

def ask(question: str, k: int = 3) -> str:
    print(f"Ищем информацию по вопросу: '{question}'...")
    # 1. Превращаем вопрос в вектор
    q_vec = embed([question])[0]
    # 2. Ищем похожие куски в базе
    hits = search(q_vec, k=k)
    
    print("Генерируем ответ через GigaChat...")
    # 3. Отправляем найденные куски и вопрос в GigaChat
    answer = generate_answer(question, hits)
    
    # 4. Собираем ссылки на источники
    sources = "; ".join(f"{h['source']}, стр. {h['page']}" for h in hits)
    return f"{answer}\n\nИсточники: {sources}"

def run_demo():
    # Вопросы для демонстрации на защите
    DEMO_QUESTIONS = [
        "О чём этот документ?",                 
        "Что такое RAG и как он работает?",        
        "Какой университет основал автор?",   # Вопроса нет в тексте (проверка на галлюцинации)
        "Что токое искуственый интелект?"     # Вопрос с опечатками
    ]
    for i, q in enumerate(DEMO_QUESTIONS, 1):
        print(f"\n[{i}/{len(DEMO_QUESTIONS)}] Вопрос: {q}")
        print(ask(q))