# Todo App — Project Belajar DevOps

Aplikasi Flask (Todo list) yang di-containerize dengan Docker dan punya pipeline CI/CD via GitHub Actions.

## Struktur

```
DevSecOps/
├── app/                 # Aplikasi Flask (app.py + template)
├── tests/               # Test pytest
├── .github/workflows/   # Pipeline CI/CD
├── k8s/                 # Manifes Kubernetes (deployment + service)
├── terraform/           # Infrastructure as Code (Docker provider)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Menjalankan Lokal (tanpa Docker)

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt   # deps dev (test, bandit, pip-audit)
PORT=5000 .venv/bin/python -m app.app
# buka http://localhost:5000
```

Note: `requirements.txt` berisi production deps saja (runtime). `requirements-dev.txt` berisi tools pengembangan (pytest, bandit, pip-audit) — di-install hanya saat development & CI.

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

## Kubernetes

Deploy aplikasi ke cluster (minikube/K8s):

```bash
minikube start
minikube image build -t todo-app:latest .
minikube kubectl -- apply -f k8s/
minikube kubectl -- get pods
minikube service todo-web --url
```

Scaling & update:
```bash
minikube kubectl -- scale deployment todo-web --replicas=3
minikube kubectl -- rollout restart deployment todo-web
minikube kubectl -- rollout undo deployment todo-web
```

## Terraform (IaC)

Provision container/network/volume dari kode (Docker provider):

```bash
cd terraform
terraform init      # unduh provider
terraform plan      # lihat rencana
terraform apply     # bikin resource
terraform destroy   # hapus semua

# override variabel saat deploy
terraform apply -var="container_count=4" -var="app_port=9000"
```

Variabel & output didefinisikan di `variables.tf` dan `main.tf`.
