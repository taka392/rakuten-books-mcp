"""Smoke-test Rakuten Books Web Service."""
from __future__ import annotations

import json
import sys

from .client import RakutenBooksClient, RakutenBooksError


def _dump(label: str, payload: object) -> None:
    print(f"\n=== {label} ===")
    print(json.dumps(payload, ensure_ascii=False, indent=2)[:4000])


def main() -> int:
    try:
        client = RakutenBooksClient()
    except RakutenBooksError as exc:
        print(f"Setup error: {exc}", file=sys.stderr)
        return 1

    try:
        _dump("verify (BooksGenre root)", client.verify())
        _dump("search_books (sample title)", client.books_book_search(title="Python", hits=3))
    except RakutenBooksError as exc:
        print(f"API error: {exc}", file=sys.stderr)
        return 1

    print("\nOK: end-to-end Rakuten Books Web Service access works.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
