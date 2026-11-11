def load_pages(file_path: str) -> list[dict]:
    pages = []
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
        if text:
            pages.append({"text": text, "page": 1})
    return pages