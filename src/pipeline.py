from src.pdf_loader import load_pages
from src.chunker import chunk_text
from src.embedder import embed
from src.vector_store import add_chunks

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
                # Берем только имя файла (article.txt), без полного пути
                "source": file_path.split("/")[-1].split("\\")[-1], 
                "chunk_id": i,
            })
            
    print(f"   Получено {len(all_chunks)} чанков.")
    print("3. Создаем эмбеддинги (это может занять время)...")
    vectors = embed([c["text"] for c in all_chunks])
    
    print("4. Сохраняем в базу данных...")
    add_chunks(all_chunks, vectors)
    
    print(f"УСПЕХ! Файл {file_path} проиндексирован.")