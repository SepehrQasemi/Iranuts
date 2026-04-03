# 02 Architecture Map

## Repository structure tree

Simplified tree of the current repository:

```text
Iranuts-main/
├── accounts/
│   ├── admin.py
│   ├── forms.py
│   ├── managers.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── blog/
│   ├── admin.py
│   ├── migrations/
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── mixins.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docs/
│   ├── architecture.md
│   ├── refactor_audit.md
│   └── audit/
├── media/
├── Shop/
│   ├── admin.py
│   ├── forms.py
│   ├── migrations/
│   ├── models.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── static/
├── templates/
│   ├── registration/
│   └── *.html
├── .env.example
├── .gitignore
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt
```

## Django project/app relationships

### Root project

- Django project package: `config`
- Entry point: `manage.py`
- Installed business apps:
  - `accounts`
  - `Shop`
  - `blog`

### Dependency direction

Observed relationships:

- `accounts` depends on `Shop` because a post-save signal auto-creates a `Shop.Cart`
- `Shop` depends on `accounts` through `settings.AUTH_USER_MODEL`
- `blog` depends on `accounts` because `Post.author` points to the custom user model
- `config` provides cross-cutting concerns such as routing and permission mixins

This is a typical small Django monolith, but the coupling is tighter than ideal.

## Important settings/config files

### `config/settings.py`

Important behaviors:

- uses a custom `.env` loader instead of `django-environ`
- reads:
  - `DJANGO_SECRET_KEY`
  - `DJANGO_DEBUG`
  - `DJANGO_ALLOWED_HOSTS`
- defaults are local-dev friendly
- uses SQLite
- sets `AUTH_USER_MODEL = "accounts.CustomUser"`
- uses top-level `templates/`
- stores uploads in `media/`

### `config/urls.py`

Responsibilities:

- mounts `Shop.urls` at root
- mounts `accounts.urls` at `accounts/`
- mounts `django.contrib.auth.urls` at `accounts/`
- mounts `blog.urls` at root
- serves media files through Django URL helpers

### `config/mixins.py`

Provides:

- `AdminRequiredMixin`
- `UserOwnsObjectOrAdminMixin`

This file is important because permission logic is not centralized in a policy layer anywhere else.

## URL routing map

High-level route map from Django URL inspection:

### Root / storefront

- `/`
- `/HomePage/`
- `/ContactUs/`
- `/AboutUs/`
- `/Search/`

### Profile/account

- `/accounts/signup/`
- `/accounts/login/`
- `/accounts/logout/`
- `/accounts/logedin/`
- `/Profile/<pk>/`
- `/ProfileEdit/<pk>/`

### Catalog

- `/ProductView/`
- `/ProductCreate/`
- `/ProductEdit/<pk>/`
- `/ProductDelete/<pk>/`
- `/ProductDetail/<pk>/`
- `/CategoryView/`
- `/CategoryDetail/<pk>/`
- `/CategoryCreate/`
- `/CategoryEdit/<pk>/`
- `/CategoryDelete/<pk>/`

### Supplier/inventory

- `/SupplierView/`
- `/SupplierCreate/`
- `/SupplierEdit/<pk>/`
- `/SupplierDelete/<pk>/`
- `/SupplierDetail/<pk>/`
- `/InventoryView/`
- `/InventoryCreate/`
- `/InventoryEdit/<pk>/`
- `/InventoryDelete/<pk>/`
- `/InventoryDetail/<pk>/`
- `/InventoryProduct/`
- `/InventoryProductCreate/`
- `/InventoryProductDetail/<pk>/`
- `/InventoryProductEdit/<pk>/`
- `/InventoryProductDelete/<pk>/`

### Cart/order

- `/addtocart/`
- `/Cart/<pk>/`
- `/CartEdit/<cart_item_id>/`
- `/CartDelete/<cart_item_id>/`
- `/OrderCreate/`
- `/Order/`
- `/Order/update/<pk>/`

### Blog

- `/blog/`
- `/blog/Post/<pk>`
- `/new_post/`
- `/PostEdit/<pk>/`
- `/PostDelete/<pk>/`

## Template organization

Template organization is functional but inconsistent.

### Current structure

- almost all templates live flat under `templates/`
- auth templates live under `templates/registration/`
- template names are mixed:
  - `Base.html`
  - `ProductView.html`
  - `CartView.html`
  - `PostDetails.html`
  - `Profile.html`

### Observations

- naming does not follow a strong app-based namespace convention
- some templates are clearly tied to admin CRUD, but are not grouped that way
- `templates/InventoryView.html` looks suspiciously incomplete
- `templates/Users.html` looks like a leftover/demo page, not a real project asset

## Static/media organization

### `static/`

Holds shared static assets referenced from the main base template.

### `media/`

Configured as upload storage for image fields such as:

- `Product.image`
- `Category.image`

### Concerns

- media is present in the repo workspace
- local uploaded files should generally not be versioned for portfolio/public use

## Forms / models / views / admin structure

### Forms

- `accounts/forms.py` contains signup logic
- `Shop/forms.py` contains generic `ModelForm` classes for admin CRUD
- `blog` currently relies mostly on generic view `fields` declarations instead of dedicated forms

### Models

- domain models are concentrated in `Shop/models.py`
- `accounts` owns the custom user model
- `blog` owns a single `Post` model

### Views

- `Shop/views.py` is the main control center
- it mixes:
  - public pages
  - admin CRUD
  - cart/order transactional endpoints
- `accounts/views.py` is relatively small
- `blog/views.py` is simple and mostly CRUD-oriented

### Admin

- all apps use basic `admin.site.register(...)`
- there is little evidence of careful admin UX or admin-side validation hardening

## Where business logic actually lives

### Current primary locations

- `Shop/services.py`
  - cart mutation
  - cart item update
  - order creation and inventory decrement
- `Shop/views.py`
  - request parsing
  - messages
  - redirects
  - permission gating
- `accounts/models.py`
  - post-save signal creates a cart for every new user

### Important conclusion

The project is no longer pure “fat view + passive model”, but it is also not fully layered.

Business logic currently lives in three places:

- service functions
- view methods/functions
- signals

That split is workable, but it shows partial architectural transition rather than a settled design.

## Signs of architectural drift or inconsistency

Concrete signs of drift:

- old migration history includes temporary models such as `Form` and renamed location fields
- route and template naming are inconsistent
- profile routes are located in `Shop/urls.py` even though the views live in `accounts`
- a custom login success page `logedin` exists alongside standard Django auth routes
- tests and service layer look newer than the rest of the codebase
- the workspace contains newer audit/refactor docs that do not match a dormant legacy repository
- an empty `Iranuts/` directory still exists

## Architecture assessment

The architecture is understandable, but not cleanly separated.

Strengths:

- single Django monolith is easy to boot mentally
- domain is visible in the model layer
- recent service extraction improved the critical order path

Weaknesses:

- flat templates
- mixed naming
- mixed concerns in `Shop/views.py`
- tight coupling between apps
- signs of several unfinished or historically replaced ideas
