# Cleanup legacy Django storefront and add one-click local run workflow

## Summary

This branch takes the legacy Iranuts Django monolith from an audited but uneven state to a cleaner, verified, and review-ready state without rewriting its architecture. The work focuses on correctness, maintainability, local developer experience, and honest portfolio presentation.

## Major changes

- cleaned auth/profile flow:
  - explicit login/logout routes
  - phone-based login UX cleanup
  - canonical profile routes under `accounts`
  - legacy profile URLs preserved through redirects
- hardened order history:
  - `Order.is_send` renamed to `is_sent`
  - `OrderItem` now stores immutable `unit_price` and `line_total`
  - transactional order creation continues through the service layer
- improved cart/order/inventory flow clarity:
  - service-layer mutations retained in `Shop/services.py`
  - quantity and ownership checks covered by tests
- upgraded admin usability:
  - focused `ModelAdmin` classes for core storefront, inventory, order, blog, and user models
- reorganized templates:
  - namespaced template directories for `accounts`, `blog`, `shared`, and `shop`
  - cleaned `Base.html`
  - removed legacy/suspicious leftovers such as `templates/Users.html`
- added one-click local run workflow:
  - `RUN_ME.ps1`
  - `RUN_ME.bat`
  - `docs/run_local.md`
- expanded regression tests for the main business and auth flows
- updated README and cleanup docs for portfolio-ready presentation

## Verification

Executed successfully in the repository root:

```powershell
python --version
python -m pip install -r requirements.txt
python manage.py check
python manage.py makemigrations --check
python manage.py migrate
python manage.py test
PowerShell -ExecutionPolicy Bypass -File .\RUN_ME.ps1 -SetupOnly -NoBrowser
cmd /c RUN_ME.bat -SetupOnly -NoBrowser
```

HTTP smoke checks after launcher boot:

- `/` -> `200`
- `/ProductView/` -> `200`
- `/blog/` -> `200`
- `/accounts/login/` -> `200`
- `/accounts/signup/` -> `200`

## Known limitations

- still a legacy server-rendered Django monolith
- still uses SQLite for local development
- route names like `/ProductView/` remain for compatibility
- cart auto-creation via signal still exists
- no payment or shipping workflow
- browser automation via Playwright MCP is blocked in this environment by:
  - `EPERM: operation not permitted, mkdir 'C:\\Windows\\System32\\.playwright-mcp'`
