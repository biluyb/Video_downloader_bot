# Security

## Token Security

- `BOT_TOKEN` is loaded **only** from environment variables or `.env`
- The `.env` file is in `.gitignore` — never committed
- `main.py` rejects placeholder tokens at startup
- **Never** put the token in source code, README, docs, tests, Docker config, or logs

## URL Security (FEATURE-002+)

### Allowed
- `http://` and `https://` schemes only

### Rejected
- `file://`, `javascript:`, `data:`, `gopher://`, `ftp://`
- `localhost`, `127.0.0.1`, `::1`
- Private IP ranges (`10.x`, `172.16–31.x`, `192.168.x`)
- Link-local addresses (`169.254.x`)
- Internal hostnames

### SSRF Protection
- DNS resolution is validated before download
- No user-controlled redirects to internal services

## Command Injection Protection

- **Never** use `os.system()` or `shell=True`
- All subprocesses use `asyncio.create_subprocess_exec()` with argument arrays
- User input is **never** interpolated into shell commands

## File Security

- User-provided filenames are **never** used as filesystem paths
- Every download gets a unique job directory: `downloads/<job_id>/`
- Path traversal (`../`) is rejected
- Filenames are sanitised before writing

## Resource Protection

| Limit | Default | Configurable |
|---|---|---|
| Max concurrent downloads | 2 | ✅ |
| Max concurrent per user | 1 | ✅ |
| Max concurrent per group | 1 | ✅ |
| Max queue size | 20 | ✅ |
| Max file size | 500 MB | ✅ |
| Max video duration | 30 min | ✅ |
| Downloads per hour / user | 10 | ✅ |
| Download timeout | 1800 s | ✅ |

## Data Privacy

- Only operational data is stored (user ID, download metadata)
- Message contents are not stored
- No authentication cookies or private credentials
- Downloaded media is deleted immediately after upload
