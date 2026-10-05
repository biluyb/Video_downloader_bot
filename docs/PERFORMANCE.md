# Performance

## Async Design

- The bot uses `asyncio` throughout — the event loop is never blocked
- All I/O operations (Telegram API, file system, subprocess) are async
- Downloads and FFmpeg processing run as background tasks

## Concurrency Control

| Setting | Default |
|---|---|
| `MAX_CONCURRENT_DOWNLOADS` | 2 |
| `MAX_CONCURRENT_PER_USER` | 1 |
| `MAX_CONCURRENT_PER_GROUP` | 1 |
| `MAX_QUEUE_SIZE` | 20 |

## Resource Efficiency

- Large files are streamed, never loaded entirely into RAM
- Temporary files are cleaned immediately after upload
- Progress updates are throttled to every 2–5 seconds
- Third-party log noise is suppressed

## Scalability Path

1. **Current**: SQLite + single process
2. **Next**: PostgreSQL + connection pooling
3. **Future**: Multiple workers, Redis queue, horizontal scaling
