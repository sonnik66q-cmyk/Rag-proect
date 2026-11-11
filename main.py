import argparse
from src.pipeline import ingest, ask, run_demo

def main():
    parser = argparse.ArgumentParser(description="RAG-система по вашему документу")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Команда ingest (загрузка документа)
    ingest_parser = subparsers.add_parser("ingest", help="Загрузить документ в базу")
    ingest_parser.add_argument("file", type=str, help="Путь к файлу (например, data/article.txt)")

    # Команда ask (задать вопрос)
    ask_parser = subparsers.add_parser("ask", help="Задать вопрос по документу")
    ask_parser.add_argument("question", type=str, help="Текст вашего вопроса")
    ask_parser.add_argument("--k", type=int, default=3, help="Количество чанков для поиска (по умолчанию 3)")

    # Команда demo (прогон тестов)
    subparsers.add_parser("demo", help="Запустить демо-вопросы")

    args = parser.parse_args()

    if args.command == "ingest":
        ingest(args.file)
    elif args.command == "ask":
        print(ask(args.question, k=args.k))
    elif args.command == "demo":
        run_demo()

if __name__ == "__main__":
    main()