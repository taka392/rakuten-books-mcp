"""Rakuten Books Web Service API client (applicationId + accessKey)."""
from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

API_ROOT = "https://openapi.rakuten.co.jp/services/api"
BOOKS_BOOK_SEARCH = f"{API_ROOT}/BooksBook/Search/20170404"
BOOKS_GENRE_SEARCH = f"{API_ROOT}/BooksGenre/Search/20121128"


class RakutenBooksError(RuntimeError):
    """Raised when the Rakuten Books API returns an error."""


class RakutenBooksClient:
    """Books Book Search + Books Genre Search.

    Credentials are read from environment (typically MCP ``env`` block):

    - ``RAKUTEN_BOOKS_APPLICATION_ID`` — Application ID from the developer portal
    - ``RAKUTEN_BOOKS_ACCESS_KEY`` — Access Key (sent as ``accessKey`` header)
    - ``RAKUTEN_BOOKS_AFFILIATE_ID`` — optional; adds ``affiliateId`` to requests
    """

    def __init__(
        self,
        application_id: Optional[str] = None,
        access_key: Optional[str] = None,
        affiliate_id: Optional[str] = None,
    ) -> None:
        self.application_id = (
            application_id or os.getenv("RAKUTEN_BOOKS_APPLICATION_ID", "")
        ).strip()
        self.access_key = (
            access_key or os.getenv("RAKUTEN_BOOKS_ACCESS_KEY", "")
        ).strip()
        self.affiliate_id = (
            affiliate_id or os.getenv("RAKUTEN_BOOKS_AFFILIATE_ID", "") or ""
        ).strip()

        if not self.application_id or not self.access_key:
            raise RakutenBooksError(
                "RAKUTEN_BOOKS_APPLICATION_ID and RAKUTEN_BOOKS_ACCESS_KEY must be set. "
                "Pass them via the MCP client's env block."
            )

        self._headers = {"accessKey": self.access_key}

    def _merge_optional_affiliate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        if self.affiliate_id:
            params = {**params, "affiliateId": self.affiliate_id}
        return params

    def _get_json(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        params = self._merge_optional_affiliate(params)
        try:
            resp = requests.get(
                url,
                params=params,
                headers=self._headers,
                timeout=30,
            )
        except requests.RequestException as exc:
            raise RakutenBooksError(f"Network error calling {url}: {exc}") from exc

        try:
            data = resp.json()
        except ValueError as exc:
            raise RakutenBooksError(
                f"Non-JSON response ({resp.status_code}): {resp.text[:500]}"
            ) from exc

        if isinstance(data, dict) and data.get("error"):
            raise RakutenBooksError(
                f"Rakuten API error: {data.get('error')} — {data.get('error_description', '')}"
            )

        if resp.status_code >= 400:
            raise RakutenBooksError(
                f"HTTP {resp.status_code} on {url}: {resp.text[:500]}"
            )

        return data

    def verify(self) -> Dict[str, Any]:
        """Lightweight call: root genre tree (``booksGenreId=000``)."""
        return self.books_genre_search(books_genre_id="000", genre_path=0)

    def books_genre_search(
        self,
        books_genre_id: str = "000",
        genre_path: int = 0,
        format_version: int = 2,
    ) -> Dict[str, Any]:
        """BooksGenre/Search — genre names and hierarchy.

        Use ``books_genre_id='000'`` for top-level genres.
        """
        params: Dict[str, Any] = {
            "applicationId": self.application_id,
            "format": "json",
            "formatVersion": format_version,
            "booksGenreId": books_genre_id,
            "genrePath": genre_path,
        }
        return self._get_json(BOOKS_GENRE_SEARCH, params)

    def books_book_search(
        self,
        *,
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
        format_version: int = 2,
    ) -> Dict[str, Any]:
        """BooksBook/Search — at least one of title, author, publisher, isbn, or genre.

        See https://webservice.rakuten.co.jp/documentation/books-book-search
        """
        params: Dict[str, Any] = {
            "applicationId": self.application_id,
            "format": "json",
            "formatVersion": format_version,
            "hits": max(1, min(30, hits)),
            "page": max(1, min(100, page)),
        }
        if title:
            params["title"] = title
        if author:
            params["author"] = author
        if publisher_name:
            params["publisherName"] = publisher_name
        if isbn:
            params["isbn"] = isbn
        if books_genre_id:
            params["booksGenreId"] = books_genre_id
        if size is not None:
            params["size"] = size
        if sort:
            params["sort"] = sort
        if availability is not None:
            params["availability"] = availability
        if out_of_stock_flag is not None:
            params["outOfStockFlag"] = out_of_stock_flag

        has_criterion = any(
            k in params
            for k in ("title", "author", "publisherName", "isbn", "booksGenreId", "size")
        )
        if not has_criterion:
            raise RakutenBooksError(
                "books_book_search requires at least one of: title, author, "
                "publisher_name, isbn, books_genre_id, or size."
            )

        return self._get_json(BOOKS_BOOK_SEARCH, params)
