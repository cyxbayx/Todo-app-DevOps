# Todo App — Project Belajar DevOps

Aplikasi Flask (Todo list) yang di-containerize dengan Docker dan punya pipeline CI/CD via GitHub Actions.

## Struktur

```
DevSecOps/
├── app/                 # Aplikasi Flask (app.py + template)
├── tests/               # Test pytest
├── .github/workflows/   # Pipeline CI/CD
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Menjalankan Lokal (tanpa Docker)

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
PORT=5000 .venv/bin/python -m app.app
# buka http://localhost:5000
```

## Menjalankan dengan Docker

```bash
docker compose up -d --build
# buka http://localhost:8000
```

Data tersimpan di volume `todo-data` (file `/data/todo.db`), jadi tetap ada setelah restart.

## Test

```bash
.venv/bin/python -m pytest -q
```

## API

| Method | Path             | Deskripsi          |
|--------|------------------|--------------------|
| GET    | `/health`        | Health check       |
| GET    | `/api/todos`     | List semua todo    |
| POST   | `/api/todos`     | Tambah todo (JSON `{"title": "..."}`) |
| PATCH  | `/api/todos/<id>`| Toggle selesai     |

## CI/CD (GitHub Actions)

- **test** — jalankan di setiap push/PR ke `main`.
- **build** — (hanya push ke `main`) build & push image ke **GHCR** dengan tag `latest` dan `git sha`.

### Aktifkan job Deploy (opsional)

1. Buat repo di GitHub dan push kode ke `main`.
2. Image otomatis ter-push ke `ghcr.io/<user>/<repo>`.
3. Uncomment job `deploy` di `.github/workflows/ci.yml`.
4. Set secrets di GitHub: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`.
