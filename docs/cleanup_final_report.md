# Cleanup Final Report

## 1. What was fixed

### Auth and profile flow

- removed the dead `logedin` success-page path and its fragile localStorage-based redirect logic
- made login and logout behavior explicit through configured auth views in `config/urls.py`
- clarified the phone-based login form and labels
- moved canonical profile routes into `accounts/urls.py`
- preserved legacy root profile URLs as redirects so old links do not break immediately
- fixed signup so form-based user creation also sets the inherited `username` value to the phone number

### Template and UI consistency

- reorganized templates into namespaced folders:
  - `templates/shared/`
  - `templates/accounts/`
  - `templates/accounts/registration/`
  - `templates/shop/`
  - `templates/blog/`
- cleaned `Base.html`:
  - removed hardcoded category IDs
  - made footer category links data-driven via a context processor
  - removed fragile demo/personal footer content
  - fixed the visible encoding artifact
  - changed logout to an explicit POST form
- removed suspicious leftovers such as:
  - `templates/Users.html`
  - sparse legacy inventory/list templates
  - dead `templates/registration/*` redirect templates

### Naming cleanup

- renamed `Order.is_send` to `Order.is_sent`
- renamed `Post.summaries` to `Post.summary`
- normalized cart/order route names while keeping legacy public paths stable

### Order-history hardening

- added immutable `unit_price` and `line_total` fields to `OrderItem`
- captured price snapshots during order creation
- backfilled new pricing fields for existing order rows through a migration
- updated admin and templates to display snapshot values instead of depending on mutable product prices

### Admin hardening

- replaced mostly raw model registration with focused `ModelAdmin` classes for:
  - `CustomUser`
  - `Category`
  - `Product`
  - `Province`
  - `Inventory`
  - `InventoryProduct`
  - `Supplier`
  - `Cart`
  - `CartItem`
  - `Order`
  - `OrderItem`
  - `Post`
- added practical `list_display`, `search_fields`, `list_filter`, `readonly_fields`, and order-item inline visibility

## 2. What was improved

- the main cart/order/inventory mutations stay in `Shop/services.py` instead of drifting back into views
- `Shop/views.py` now has clearer internal helper functions for redirect and validation-message handling
- blog create/edit flows now use a dedicated form and automatically assign `author` from `request.user`
- shared navigation/footer categories are exposed consistently through `config.context_processors.navigation`
- repository hygiene was improved by ignoring local database/media/cache artifacts instead of tracking them
- README now frames the repository honestly as a legacy cleanup case study rather than pretending it is a production commerce system

## 3. What was intentionally left unchanged

- the monolith was not split into more Django apps
- SQLite was kept for local development
- migration history was not rewritten
- public URL paths such as `/ProductView/` and `/CategoryView/` were kept to avoid broad route churn
- the automatic cart-creation signal was retained
- the project was not converted to DRF, React, Vue, Docker, Celery, or another architecture
- no fake payment, shipment tracking, or other advanced commerce features were added

## 4. One-click run workflow added

The repository now includes a Windows-friendly one-click local workflow:

- `RUN_ME.ps1`
- `RUN_ME.bat`
- `docs/run_local.md`

The launcher:

1. checks that Python is available
2. creates or reuses `.venv`
3. installs requirements when needed
4. creates `.env` from `.env.example` if missing
5. runs database migrations
6. optionally opens the local app in the default browser
7. starts the Django development server

Verified paths:

- `PowerShell -ExecutionPolicy Bypass -File .\\RUN_ME.ps1 -SetupOnly -NoBrowser`
- `cmd /c RUN_ME.bat -SetupOnly -NoBrowser`
- full launcher boot followed by HTTP smoke checks against the running app

## 5. Migrations created

- `Shop/migrations/0021_refactor_cart_order_logic.py`
- `Shop/migrations/0023_alter_order_address_alter_order_province_and_more.py`
- `Shop/migrations/0024_orderitem_price_snapshot_and_order_is_sent.py`
- `blog/migrations/0005_rename_summaries_to_summary.py`

## 6. Tests added or updated

### `accounts/tests.py`

- signup creates a user and cart
- phone-based login redirects correctly
- logout redirects correctly
- profile owner vs non-owner access control

### `Shop/tests.py`

- storefront page render smoke tests
- add-to-cart merge behavior through the view
- cart update/delete view behavior
- cart ownership protection
- order creation success with price snapshots
- insufficient inventory rejection
- admin-only page protection

### `blog/tests.py`

- public blog list/detail rendering
- admin write-path protection
- admin post creation with automatic author assignment

## 7. Commands run

```powershell
git rev-parse --is-inside-work-tree
git remote -v
git branch --show-current
git status --short
python --version
python -m pip install -r requirements.txt
python manage.py check
python manage.py makemigrations --check
python manage.py migrate
python manage.py test
PowerShell -ExecutionPolicy Bypass -File .\RUN_ME.ps1 -SetupOnly -NoBrowser
cmd /c RUN_ME.bat -SetupOnly -NoBrowser
git push -u origin cleanup/portfolio-hardening
```

### Launcher smoke verification

```powershell
Start-Process PowerShell -ArgumentList '-ExecutionPolicy','Bypass','-File','C:\dev\Iranuts\RUN_ME.ps1','-NoBrowser'
Invoke-WebRequest http://127.0.0.1:8000/
Invoke-WebRequest http://127.0.0.1:8000/ProductView/
Invoke-WebRequest http://127.0.0.1:8000/blog/
Invoke-WebRequest http://127.0.0.1:8000/accounts/login/
Invoke-WebRequest http://127.0.0.1:8000/accounts/signup/
```

## 8. Verification results

- `python --version`: `Python 3.11.9`
- `python -m pip install -r requirements.txt`: passed, requirements already satisfied
- `python manage.py check`: passed
- `python manage.py makemigrations --check`: passed, no model drift
- `python manage.py migrate`: passed, no remaining unapplied migrations
- `python manage.py test`: passed with 15 tests
- `RUN_ME.ps1 -SetupOnly -NoBrowser`: passed
- `RUN_ME.bat -SetupOnly -NoBrowser`: passed
- launcher boot plus HTTP smoke checks:
  - `/` -> `200`
  - `/ProductView/` -> `200`
  - `/blog/` -> `200`
  - `/accounts/login/` -> `200`
  - `/accounts/signup/` -> `200`
- `git push -u origin cleanup/portfolio-hardening`: passed

## 9. Remaining known issues

- the project is still a legacy server-rendered UI; it is cleaner and more credible now, but not highly polished
- order state is intentionally simple (`is_sent` only)
- the cart-creation signal remains a hidden side effect, even though it is now documented and test-covered
- some route names and paths still reflect the legacy project style (`ProductView`, `CategoryView`, and similar)
- there is still no payment flow, shipment tracking, or richer fulfillment model
- browser automation through the Playwright MCP browser remains blocked in this environment by:
  - `EPERM: operation not permitted, mkdir 'C:\\Windows\\System32\\.playwright-mcp'`

## 10. Manual smoke test steps

1. From the repository root, run:

```powershell
.\RUN_ME.ps1
```

2. Or double-click:

- `RUN_ME.bat`

3. If you want setup without starting the server:

```powershell
.\RUN_ME.ps1 -SetupOnly
```

4. Verify public pages:

- `/`
- `/ProductView/`
- `/CategoryView/`
- `/blog/`
- `/accounts/login/`
- `/accounts/signup/`

5. Verify account flow:

- sign up a new user
- log in with the phone number
- open `/accounts/profile/<id>/`
- edit the profile

6. Verify cart/order flow:

- open a product detail page
- add the product to the cart
- update quantity
- remove and re-add an item
- submit an order with a province that has stock

7. Verify admin flow:

- create a superuser if needed
- open `/admin/`
- review Product, InventoryProduct, Order, Supplier, Category, Post, and CustomUser admin screens
- confirm `OrderItem` shows `unit_price` and `line_total`

8. Re-run regression checks if you want to confirm the local environment:

```powershell
python manage.py check
python manage.py test
```

## 11. Branch name

- `cleanup/portfolio-hardening`

## 12. Push status

- pushed successfully to `origin/cleanup/portfolio-hardening`
- GitHub compare/PR URL:
  - `https://github.com/SepehrQasemi/Iranuts/pull/new/cleanup/portfolio-hardening`
