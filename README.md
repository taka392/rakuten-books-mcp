# rakuten-books-mcp

MCP server for the [Rakuten Books Web Service](https://webservice.rakuten.co.jp/documentation/books-book-search).

Exposes:

| Tool | API |
|------|-----|
| `verify` | `BooksGenre/Search` with `booksGenreId=000` (credential check) |
| `search_book_genres` | `BooksGenre/Search` |
| `search_books` | `BooksBook/Search` |

Credentials are **not** read from `.env` at runtime. Pass them via your MCP client’s `env` block (e.g. `~/.cursor/mcp.json`).

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `RAKUTEN_BOOKS_APPLICATION_ID` | yes | Application ID from the [developer portal](https://webservice.rakuten.co.jp/) |
| `RAKUTEN_BOOKS_ACCESS_KEY` | yes | Access Key (sent as query parameter `accessKey`, per current Open API behaviour) |
| `RAKUTEN_BOOKS_AFFILIATE_ID` | no | Affiliate ID — when set, `affiliateId` is added and responses may include `affiliateUrl` |

The client sends `Origin` / `Referer` as `https://www.rakuten.co.jp/` so calls to `openapi.rakuten.co.jp` do not fail with `REQUEST_CONTEXT_BODY_HTTP_REFERRER_MISSING` (403).

If Cursor still runs an old `uvx` cache, add `"--refresh"` before `"--from"` in `mcp.json` (already recommended in the example flow).

## Security

If an Application ID or Access Key was pasted into a chat or committed by mistake, **regenerate the Access Key** (or recreate the app) in the Rakuten developer portal before use.

## Prerequisites

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) / `uvx` (recommended). On macOS: `brew install uv`
- A Rakuten Web Service app with **Book API** enabled

## Register with Cursor

Merge under `mcpServers` in `~/.cursor/mcp.json` (see [`examples/cursor_mcp_config.example.json`](examples/cursor_mcp_config.example.json)).

Use the full path to `uvx` if Cursor reports `spawn uvx ENOENT`:

```json
"command": "/opt/homebrew/bin/uvx"
```

Reload the window (`Cmd+Shift+P` → **Developer: Reload Window**).

## Smoke test (CLI)

```bash
cd rakuten-books-mcp
python3.11 -m venv .venv && source .venv/bin/activate
pip install -e .

export RAKUTEN_BOOKS_APPLICATION_ID=...
export RAKUTEN_BOOKS_ACCESS_KEY=...
export RAKUTEN_BOOKS_AFFILIATE_ID=...   # optional

rakuten-books-mcp-check
```

## Local dev (stdio)

```bash
source .venv/bin/activate
rakuten-books-mcp
```

## Documentation

- [Books Book Search API](https://webservice.rakuten.co.jp/documentation/books-book-search)
- [Books Genre Search API](https://webservice.rakuten.co.jp/documentation/books-genre-search)

## License

MIT — see [`LICENSE`](LICENSE).
