# 01 Project Overview

## Project identity

- Repository name: `Iranuts-main`
- Framework: Django 4.2.2 on Python 3.11.9
- Current state audited: the current workspace, not a pristine 3-year-old snapshot
- Important caveat:
  - The repository already contains newer stabilization work such as `Shop/services.py`, test files, `.env.example`, and recent migrations.
  - This audit therefore describes the project as it exists now, while still calling out evidence of older legacy structure and drift.

## Likely business/domain purpose

This project appears to be a small Django e-commerce / inventory-management application for selling products by category, maintaining province-based inventory, collecting carts, and creating orders.

The strongest domain evidence is in:

- `Shop/models.py`
- `Shop/views.py`
- `templates/ProductDetail.html`
- `templates/CartView.html`
- `templates/OrderView.html`

The domain looks closer to a university-built storefront plus back-office admin panel than a production retail system. It combines:

- public product browsing
- account signup/login
- cart and order placement
- province-specific inventory
- supplier records
- a small blog/news section

## Main Django apps

### `Shop`

Primary business app. Owns most domain models and most user/admin flows.

Responsibilities:

- product catalog
- categories
- suppliers
- inventory and inventory-product join records
- cart and cart items
- orders and order items
- storefront pages such as home/search/about/contact

### `accounts`

Authentication and profile app.

Responsibilities:

- custom user model
- signup flow
- profile view/edit flow
- integration with Django auth views

### `blog`

Peripheral content app.

Responsibilities:

- blog post list/detail
- admin-managed blog CRUD

### `config`

Django project configuration.

Responsibilities:

- settings
- root URL routing
- shared permission mixins

## Core entities

The central data model revolves around:

- `CustomUser`
- `Product`
- `Category`
- `Province`
- `Inventory`
- `InventoryProduct`
- `Cart`
- `CartItem`
- `Order`
- `OrderItem`
- `Supplier`

These entities form the real business core. The `blog.Post` model is peripheral.

## Main user roles

### Anonymous visitor

Likely capabilities:

- browse products and categories
- read blog posts
- view informational pages

### Authenticated customer

Likely capabilities:

- sign up and log in using phone number
- view/edit own profile
- add products to cart
- update/delete cart items
- create orders

### Superuser / admin

Likely capabilities:

- create/edit/delete products
- manage categories
- manage suppliers
- manage inventories and stock levels
- view and mark orders as sent
- manage blog posts

Evidence for the admin split exists in `config/mixins.py` and multiple `AdminRequiredMixin`-based views in `Shop/views.py` and `blog/views.py`.

## Main features

- Custom phone-based authentication with `accounts.CustomUser`
- Automatic cart creation for new users via signal
- Product/category browsing
- Search across product and category names
- Add-to-cart flow
- Cart merge/update/delete behavior
- Province-based order creation with inventory checks
- Admin CRUD for catalog/inventory/suppliers/blog
- Public blog listing and detail pages

## What this project is not

Based on current evidence, this project is not:

- a full marketplace with vendor self-service
- a payment-integrated commerce system
- a shipment/tracking platform
- a modern REST API backend
- a well-layered enterprise Django application
- a polished production-ready storefront

It is better understood as a legacy academic Django monolith with a retail/inventory theme.

## Overall reading

The project has a coherent core business purpose and enough domain structure to be understandable and potentially portfolio-worthy. However, it also shows clear signs of being built incrementally over time:

- mixed naming styles
- flat templates
- older migration drift
- weak presentation consistency
- limited test coverage
- evidence of earlier broken or incomplete patterns

That makes it salvageable, but not clean by default.
