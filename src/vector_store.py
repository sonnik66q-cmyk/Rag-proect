import chromadb

_client = None
_collection = None

def get_collection():
    global _client, _collection
    if _client is None:
        _client = chromadb.PersistentClient(path="./chroma_db")
        _collection = _client.get_or_create_collection(name="article")
    return _collection

def add_chunks(chunks: list[dict], embeddings: list[list[float]]):
    collection = get_collection()
    ids = [f"{c['source']}_p{c['page']}_c{c['chunk_id']}" for c in chunks]
    collection.upsert(
        ids=ids,
        documents=[c["text"] for c in chunks],
        embeddings=embeddings,
        metadatas=[{"page": c["page"], "source": c["source"]} for c in chunks],
    )

def search(query_embedding: list[float], k: int = 3) -> list[dict]:
    collection = get_collection()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas"],
    )
    return [
        {"text": doc, "page": m["page"], "source": m["source"]}
        for doc, m in zip(results["documents"][0], results["metadatas"][0])
    ]