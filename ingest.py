import os
from src.pdf_loader import load_pages
from src.chunker import chunk_text
from src.embedder import embed
from src.vector_store import add_chunks


def ingest(path: str):
    # 1. Читаем документ (текст по страницам)
    pages = load_pages(path)

    # 2. Режем на чанки
    chunks = []
    for p in pages:
        for i, c in enumerate(chunk_text(p["text"])):
            chunks.append({
                "text": c,
                "page": p["page"],
                "source": os.path.basename(path),
                "chunk_id": i,
            })

    if not chunks:
        print("Нет чанков для индексации")
        return

    # 3. Векторизуем
    vectors = embed([c["text"] for c in chunks])

    # 4. Пишем в ChromaDB
    add_chunks(chunks, vectors)
    print(f"Проиндексировано чанков: {len(chunks)}")


if __name__ == "__main__":
    ingest(os.getenv("DOC_PATH", "data/article.txt"))