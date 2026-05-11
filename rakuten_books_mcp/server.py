"""Rakuten Books Web Service MCP server (FastMCP)."""
from __future__ import annotations

from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP

from .client import RakutenBooksClient, RakutenBooksError


mcp = FastMCP("rakuten-books")


def _client() -> RakutenBooksClient:
    try:
        return RakutenBooksClient()
    except RakutenBooksError as exc:
        raise RuntimeError(str(exc)) from exc


@mcp.tool()
def verify() -> Dict[str, Any]:
    """Verify credentials by calling BooksGenre/Search with booksGenreId=000.

    Returns genre metadata when applicationId and accessKey are valid.
    """
    return _client().verify()


@mcp.tool()
def search_book_genres(
    books_genre_id: str = "000",
    genre_path: int = 0,
) -> Dict[str, Any]:
    """Look up Rakuten Books genre tree.

    Args:
        books_genre_id: Genre id; use ``000`` for root-level genres.
        genre_path: 1 to include ancestor genres in the response.
    """
    return _client().books_genre_search(
        books_genre_id=books_genre_id,
        genre_path=genre_path,
    )


@mcp.tool()
def search_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    publisher_name: Optional[str] = None,
    isbn: Optional[str] = None,
    books_genre_id: Optional[str] = None,
    size: Optional[int] = None,
    hits: int = 10,
    page: int = 1,
    sort: Optional[str] = None,
    availability: Optional[int] = None,
    out_of_stock_flag: Optional[int] = None,
) -> Dict[str, Any]:
    """Search Rakuten Books (BooksBook/Search).

    At least one filter is required: title, author, publisher_name, isbn,
    books_genre_id, or size (see Rakuten docs for ``size`` codes).

    Args:
        title: Book title (UTF-8; spaces for multi-keyword).
        author: Author name.
        publisher_name: Publisher name.
        isbn: ISBN / book code.
        books_genre_id: Rakuten Books genre id (not Ichiba genre).
        size: Book format filter (0–10 per API docs).
        hits: Results per page (1–30, default 10).
        page: Page number (1–100).
        sort: e.g. ``standard``, ``sales``, ``+itemPrice``, ``-releaseDate``.
        availability: Stock filter (0–6 per API docs).
        out_of_stock_flag: 0 exclude unavailable, 1 include.
    """
    return _client().books_book_search(
        title=title,
        author=author,
        publisher_name=publisher_name,
        isbn=isbn,
        books_genre_id=books_genre_id,
        size=size,
        hits=hits,
        page=page,
        sort=sort,
        availability=availability,
        out_of_stock_flag=out_of_stock_flag,
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
