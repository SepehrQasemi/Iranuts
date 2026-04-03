# Screenshots Report

## 1. Branch name

- `docs/add-screenshots`

## 2. App run method used

- primary setup method: `RUN_ME.ps1 -SetupOnly -NoBrowser`
- primary runtime method for capture: `RUN_ME.ps1 -NoBrowser -Port 8001`

## 3. Commands run

```powershell
git fetch origin
git checkout main
git pull --ff-only origin main
git checkout -b docs/add-screenshots
python --version
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py test
PowerShell -ExecutionPolicy Bypass -File .\RUN_ME.ps1 -SetupOnly -NoBrowser
PowerShell -ExecutionPolicy Bypass -File .\RUN_ME.ps1 -NoBrowser -Port 8001
Invoke-WebRequest http://127.0.0.1:8001/
Invoke-WebRequest http://127.0.0.1:8001/ProductView/
Invoke-WebRequest http://127.0.0.1:8001/ProductDetail/1/
Invoke-WebRequest http://127.0.0.1:8001/blog/
Invoke-WebRequest http://127.0.0.1:8001/accounts/login/
Invoke-WebRequest http://127.0.0.1:8001/accounts/signup/
git push -u origin docs/add-screenshots
```

Additional local-only commands were used to:

- generate placeholder media images for screenshots
- seed a minimal local demo dataset
- capture screenshots through a temporary Playwright workspace outside the repository

## 4. Pages captured

- home page
- product list page
- product detail page
- cart page
- blog page
- admin page

## 5. Screenshot file paths

- `docs/screenshots/home.png`
- `docs/screenshots/product-list.png`
- `docs/screenshots/product-detail.png`
- `docs/screenshots/cart.png`
- `docs/screenshots/blog.png`
- `docs/screenshots/admin.png`

## 6. README/docs changes made

- updated `README.md` with a dedicated screenshots section
- added `docs/screenshots.md` for the full gallery
- added this report at `docs/screenshots_report.md`

## 7. Any limitations or missing pages

- screenshots were captured from local demo data, not committed seed data
- the built-in Playwright MCP browser was not usable in this session, so screenshots were captured through a temporary local Playwright install outside the repo
- the cart and admin screenshots required local login with demo accounts created only for capture
- no inventory/order admin changelist screenshot was added; the admin index was used as the representative admin view

## 8. Push status

- pushed successfully to `origin/docs/add-screenshots`

## 9. PR URL if available

- `https://github.com/SepehrQasemi/Iranuts/pull/new/docs/add-screenshots`
