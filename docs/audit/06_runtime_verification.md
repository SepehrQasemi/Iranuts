# 06 Runtime Verification

## Environment assumptions

- OS: Windows
- Shell: PowerShell
- Working directory: `C:\dev\Iranuts-main`
- Python used: system/local interpreter available as `python`
- Database used by the project: SQLite (`db.sqlite3`)

## Commands executed

The following safe verification commands were executed during the audit:

```powershell
python --version
python -m pip install -r requirements.txt
python manage.py check
python manage.py showmigrations
python manage.py makemigrations --check
python manage.py test
python manage.py runserver 127.0.0.1:8000 --noreload
python -u manage.py runserver 127.0.0.1:8000 --noreload --verbosity 2
```

Additional safe inspection commands were also used for repository reading, URL discovery, and SQLite inspection.

## Results

### Python version

- Result: success
- Summary:
  - `Python 3.11.9`

### Dependency installation

- Command:
  - `python -m pip install -r requirements.txt`
- Result: success
- Summary:
  - required packages were already installed
  - main dependencies observed:
    - `django==4.2.2`
    - `pillow==9.5.0`

### Django system checks

- Command:
  - `python manage.py check`
- Result: success
- Summary:
  - `System check identified no issues (0 silenced).`

### Migration inspection

- Command:
  - `python manage.py showmigrations`
- Result: success
- Summary:
  - migrations for built-in apps, `accounts`, `Shop`, and `blog` are applied
  - notable applied `Shop` migrations include:
    - `0021_refactor_cart_order_logic`
    - `0023_alter_order_address_alter_order_province_and_more`

### Model drift check

- Command:
  - `python manage.py makemigrations --check`
- Result: success
- Summary:
  - `No changes detected`
  - current models match migration state

### Test suite

- Command:
  - `python manage.py test`
- Result: success
- Summary:
  - `Found 5 test(s).`
  - `Ran 5 tests`
  - final status: `OK`

### Runserver startup attempt

- Commands:
  - `python manage.py runserver 127.0.0.1:8000 --noreload`
  - `python -u manage.py runserver 127.0.0.1:8000 --noreload --verbosity 2`
- Result: inconclusive
- Summary:
  - commands were attempted
  - they timed out in the audit environment before a meaningful interactive verification pass was completed
  - no browser-level smoke test was completed from these attempts

## Blocking errors

No blocking installation or Django configuration errors were encountered during the executed commands.

## Warnings

- Passing `check` and `test` does not prove that all template paths or browser flows render correctly
- current tests are narrow and do not cover all critical user/admin flows
- runserver was not fully exercised through a browser in this audit
- the audited workspace already includes newer tests and service-layer code, so runtime success reflects the current repo state, not necessarily the untouched original university version

## What was verified

### Verified

- Python runtime is available
- requirements install cleanly
- Django settings import successfully
- Django system checks pass
- migrations are applied
- current model state matches migrations
- current test suite passes
- URL configuration can be introspected successfully

### Partially verified

- main flows can be traced from URLs to views/templates/models
- the cart/order path has test evidence and clear transactional code

### Unverified

- full browser interaction across the storefront
- visual template correctness across all pages
- login/logout redirect UX involving `logedin` and `logged_out`
- supplier/inventory CRUD usability from the browser
- whether the current database contents represent realistic demo data

## Runtime-specific observations

### Dependency posture

The dependency footprint is small, which is good for an academic Django project:

- Django
- Pillow

That simplicity is a strength.

### Database contents at audit time

The SQLite database contained non-empty data in several core tables, including:

- users
- categories
- products
- provinces
- inventories
- inventory-product rows
- carts
- one blog post

It did not contain live order history or suppliers at the time of inspection.

## Honest conclusion

The current repository is runnable enough to pass Django checks and its present test suite. That is stronger evidence than “the code looks plausible,” but weaker than a full interactive verification. The project should therefore be described as:

- technically bootable in its current audited state
- partially runtime-verified
- not fully end-to-end verified
