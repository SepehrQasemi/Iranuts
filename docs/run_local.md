# Run Locally

## One-click workflow

From the repository root on Windows, run:

```powershell
.\RUN_ME.ps1
```

Or double-click:

- `RUN_ME.bat`

## What the launcher does

The launcher:

1. checks that Python is available
2. creates or reuses `.venv`
3. installs requirements when needed
4. creates `.env` from `.env.example` if missing
5. runs database migrations
6. opens the browser to the local app unless disabled
7. starts the Django development server

## Useful options

### Setup only

Prepare the environment without starting the server:

```powershell
.\RUN_ME.ps1 -SetupOnly
```

### Do not open the browser automatically

```powershell
.\RUN_ME.ps1 -NoBrowser
```

### Use a custom host/port

```powershell
.\RUN_ME.ps1 -ServerHost 127.0.0.1 -Port 8001
```

## Manual fallback

If you prefer the traditional flow:

```powershell
python -m pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

## Notes

- the launcher is intentionally Windows-friendly because this repository is maintained in a Windows-oriented environment
- it is meant for local development, not production deployment
