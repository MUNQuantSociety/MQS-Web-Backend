# MQS Web Backend (FastAPI)

Quick start for a fresh machine (Windows + PowerShell).

## 1) Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## 2) Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 3) Configure environment variables

Create a `.env` file in the project root (same folder as `requirements.txt`).
Example:

```
APP_NAME="MQS Backend"
APP_ENV=local
DEBUG=true
API_V1_PREFIX=/api/v1
CORS_ORIGINS=["http://localhost:3000"]
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/mqs
LOG_LEVEL=INFO
```

Note: `DATABASE_URL` is required by `src/services/database.py`.

## 4) Run the server

```powershell
python -m uvicorn src.app:app --reload
```

You should see output like:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## 5) Health check

Open this URL in your browser:

```
http://127.0.0.1:8000/api/v1/health
```

Expected response:

```
{"status":"ok"}
```
