# MQS Webapp Backend

## Structure
- `config/`: project configuration and settings modules
- `apps/`: domain apps (start here for new features)
- `manage.py`: Django entry point

## Setup
1. Create and activate a virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
2. Verify you are using the venv Python/pip:
   ```powershell
   where.exe python
   python -m pip -V
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and update values.
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the server:
   ```bash
   python manage.py runserver
   ```

## Freeze dependencies (optional)
Use the active venv to capture exact versions:
```powershell
python -m pip freeze > requirements.txt
```

## Settings modules
- Local: `config.settings.local` (default in `manage.py`)
- Production: `config.settings.production`

## Health check
- `GET /api/health/`
