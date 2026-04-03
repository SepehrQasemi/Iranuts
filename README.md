# IraNuts

IraNuts is a legacy Django storefront and back-office monolith that was reverse-engineered, audited, and cleaned up from an old university project. It keeps the original domain intact while improving maintainability, consistency, and correctness.

## Project Overview

The project models a small e-commerce workflow with province-based inventory:

- browse products and categories
- sign up and log in with a phone number
- maintain a customer cart
- create orders against province-specific stock
- manage products, suppliers, inventory, and orders from admin-only pages
- publish simple blog posts alongside the storefront

This repository is intentionally still a classic Django server-rendered app. It does not pretend to be a modern API/frontend split.

## Why This Repository Exists

This codebase is best understood as a legacy cleanup case study:

- the original project was built as an academic monolith
- the code was later audited and reverse-engineered
- the current version focuses on clarity, safer business logic, and portfolio readiness without rewriting the whole stack

## Features

- custom `CustomUser` model using `phone` as the login identifier
- automatic cart creation for new users
- product/category storefront pages
- province-based inventory tracking through `InventoryProduct`
- cart merge/update/delete behavior through explicit service functions
- transactional order creation with inventory validation
- immutable order-item price snapshots (`unit_price`, `line_total`)
- admin-only CRUD for products, categories, suppliers, inventory, stock levels, orders, and blog posts
- lightweight blog module

## Architecture Summary

### Apps

- `config`
  - project settings, root URLs, shared mixins, and shared template context
- `accounts`
  - custom user model, signup flow, profile pages, and phone-based login UX
- `Shop`
  - product catalog, categories, provinces, suppliers, inventory, cart, order flow, and service-layer business logic
- `blog`
  - public blog pages and admin-managed blog posts

### Main Business Logic

The most important mutations live in `Shop/services.py`:

- `add_product_to_cart`
- `update_cart_item_quantity`
- `create_order_from_cart`

Order creation remains transactional and now captures per-line price snapshots so historical orders remain meaningful after later product price changes.

## Template Structure

Templates are now grouped by concern under the shared top-level `templates/` directory:

- `templates/shared/`
- `templates/accounts/`
- `templates/accounts/registration/`
- `templates/shop/`
- `templates/blog/`

## Stack

- Python 3.11
- Django 4.2
- SQLite
- Django templates
- Bootstrap

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Copy the environment template:

```bash
copy .env.example .env
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Create an admin user if you want to access the back-office screens:

```bash
python manage.py createsuperuser
```

6. Start the development server:

```bash
python manage.py runserver
```

## One-Click Local Run

For the Windows-friendly local workflow, use one of these from the repository root:

```powershell
.\RUN_ME.ps1
```

or double-click:

- `RUN_ME.bat`

The launcher will:

- check for Python
- create or reuse `.venv`
- install requirements when needed
- create `.env` from `.env.example` if missing
- run migrations
- open the local app in the browser unless disabled
- start the Django development server

Useful options:

```powershell
.\RUN_ME.ps1 -SetupOnly
.\RUN_ME.ps1 -NoBrowser
```

Full launcher notes are in:

- `docs/run_local.md`

## Verification Commands

```bash
python manage.py check
python manage.py makemigrations --check
python manage.py test
```

## Screenshots

Representative local screenshots are available below. These were captured from a local demo dataset created only for documentation purposes. A fuller gallery with notes is available in [docs/screenshots.md](docs/screenshots.md).

### Home page

![Home page](docs/screenshots/home.png)

### Product list

![Product list](docs/screenshots/product-list.png)

### Product detail

![Product detail](docs/screenshots/product-detail.png)

### Cart

![Cart](docs/screenshots/cart.png)

### Blog

![Blog](docs/screenshots/blog.png)

### Admin

![Admin](docs/screenshots/admin.png)

## Known Limitations

- no payment integration
- no shipment tracking or advanced order states
- SQLite is used for simplicity and local development
- the UI is intentionally modest and server-rendered
- admin permissions are superuser-based rather than fine-grained role-based
- this is not a production-grade commerce platform

## Future Improvements

- add pagination and richer filtering for catalog/blog pages
- improve admin ergonomics for inventory and order fulfillment
- add broader browser-level smoke coverage
- tighten form validation around addresses and operational data
- add screenshots and a short demo walkthrough

## Audit And Cleanup Notes

Repository audit documents live under:

- `docs/audit/`

Cleanup planning and execution notes live under:

- `docs/cleanup_execution_plan.md`
- `docs/cleanup_final_report.md`
