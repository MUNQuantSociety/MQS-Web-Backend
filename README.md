# MQS Webapp Backend

## Structure
- `config/`: project configuration and settings modules
- `apps/`: domain apps (start here for new features)
- `manage.py`: Django entry point

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and update values.
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the server:
   ```bash
   python manage.py runserver
   ```

## Settings modules
- Local: `config.settings.local` (default in `manage.py`)
- Production: `config.settings.production`

## Health check
- `GET /api/health/`
