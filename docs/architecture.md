# Architecture

## Repository Shape

This project stays intentionally close to the original Django monolith structure:

- `config`
  - settings, root URLs, shared mixins, shared context processors
- `accounts`
  - custom user model, signup/profile flows, phone-based authentication forms
- `Shop`
  - storefront, inventory, cart/order workflow, admin CRUD, service layer
- `blog`
  - public post pages and admin-managed blog content
- `templates`
  - shared top-level template directory grouped by concern:
    - `shared/`
    - `accounts/`
    - `accounts/registration/`
    - `shop/`
    - `blog/`

## Main Request Flow

### Storefront

1. Root and catalog URLs are routed through `Shop/urls.py`.
2. Public views in `Shop/views.py` render server-side templates under `templates/shared/` and `templates/shop/`.
3. Shared footer/navigation data is injected by `config/context_processors.py`.

### Accounts

1. Signup and profile URLs are owned by `accounts/urls.py`.
2. Login/logout use Django auth views configured in `config/urls.py`.
3. The login form is customized so the UI is explicit about phone-based authentication.

### Cart And Order Workflow

1. Product detail pages post to `add_to_cart`.
2. `Shop/views.py` delegates cart mutation to `Shop/services.py`.
3. Cart updates and deletes remain explicit view actions with ownership checks.
4. Order creation calls `create_order_from_cart`, which:
   - opens a transaction
   - validates province-specific stock
   - creates the order
   - captures immutable price snapshots on each order item
   - decrements inventory
   - removes purchased cart lines

### Blog

1. Public blog list/detail routes live in `blog/urls.py`.
2. Admin-only create/edit/delete routes also live there.
3. Blog forms are explicit and author assignment is set from `request.user`.

## Where Business Logic Lives

### Explicit service layer

Core commerce mutations are centralized in `Shop/services.py`:

- `add_product_to_cart`
- `update_cart_item_quantity`
- `create_order_from_cart`

### Views

Views handle:

- request parsing
- permission checks
- messages and redirects
- rendering

### Signals

There is still one hidden side effect:

- new `CustomUser` instances automatically get a `Cart` via a post-save signal in `accounts/models.py`

That behavior is retained, documented, and tested, but it remains an intentional legacy compromise.

## Admin Structure

Admin registrations are now more intentional:

- `Product`, `Category`, `Supplier`, `Inventory`, `InventoryProduct`
- `Order` with inline `OrderItem` snapshots
- `CustomUser`
- `Post`

The admin remains practical rather than highly customized, but it is no longer raw default registration everywhere.

## Design Constraints

This cleanup intentionally avoids:

- splitting the monolith into more apps
- introducing APIs or frontend frameworks
- replacing SQLite for appearances
- rewriting migration history

The goal is a cleaner, safer legacy Django application, not a stack migration.
