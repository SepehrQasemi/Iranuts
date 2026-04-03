# Iranuts Refactor Audit

## Architecture summary

- `config/` contains a single Django settings module and the project URL router.
- `Shop/` is the main commerce app and currently owns products, categories, provinces, inventory, suppliers, carts, orders, and most of the public/admin views.
- `accounts/` defines a custom user model based on `AbstractUser` and auto-creates a cart on user creation.
- `blog/` contains a basic post model and CRUD views.
- `templates/` stores all templates in one shared directory instead of app-specific template namespaces.
- The current implementation mixes presentation, validation, and inventory mutation logic directly inside views, model `save()`, and model signals.

## Key bugs

- Multiple generic class-based views are incomplete and will raise `ImproperlyConfigured` because they define neither `fields` nor `form_class`.
- Several admin-only views define `test_func()` but do not inherit from `UserPassesTestMixin`, so the permission check never runs.
- `Shop/views.py` uses the wrong model in `SupplierView` (`Category` instead of `Supplier`).
- `Shop/urls.py` contains broken route definitions and naming issues:
  - malformed search path: `Search/>`
  - typo in inventory edit path: `InventoryrEdit`
  - `ProductCreate` incorrectly expects a `pk`
- `accounts` routing and templates are inconsistent:
  - `accounts/views.py` expects `profile.html`, but the actual template is `Profile.html`
  - URL names differ between `profile` and `Profile`
  - signup error handling refers to `phone_no`, while the user model uses `phone`
- The custom user manager builds `phone_no` instead of `phone`, which breaks user creation and superuser creation.
- Cart and order templates reference nonexistent fields such as `user.phone_no`, `order.city`, and `Product.inventry_set`.
- Several edit/delete templates use wrong context variable names or wrap submit buttons inside links, which breaks form submission.

## Code smells

- `Shop/views.py` contains too many unrelated responsibilities: catalog pages, profile pages, admin CRUD, cart mutation, and order creation.
- `Shop/models.py` uses wildcard imports elsewhere and contains order/inventory side effects in signals instead of explicit domain logic.
- `CartItem.save()` silently merges duplicate rows, creating hidden behavior that is hard to test and reason about.
- Order inventory changes rely on `post_save`, `pre_save`, and `post_delete` signals with partial validation and silent `pass` branches.
- Search logic uses broad `try/except` blocks that hide real errors.
- The repository contains obvious local junk:
  - `db.sqlite3`
  - `media/`
  - `__pycache__/`
  - `.vscode/`
  - `Shop/Untitled-1.sql`

## Security issues

- `SECRET_KEY` is committed in source.
- `DEBUG=True` is hardcoded.
- `ALLOWED_HOSTS` is hardcoded to an empty list instead of environment-based configuration.
- Admin-only CRUD views are inconsistently protected.
- Cart/order mutation views do not explicitly guard against invalid quantities or missing ownership errors.
- Inventory validation can fail silently during signal execution, which risks inconsistent order state.

## Maintainability issues

- Templates are flat and inconsistently named, making reverse lookups and reuse harder.
- View names, URL names, and template names are not normalized (`Profile` vs `profile`, `OrderView` vs `orders.html`, `OrderEdit.html` vs `orderupdate.html`).
- Business rules for cart merging and inventory reservation are not centralized.
- No meaningful automated tests exist.
- The current project state cannot be validated out of the box without installing dependencies, and the repo has no local environment example.

## Recommended refactor order

1. Fix runtime blockers first: broken imports, URL typos, wrong model references, missing `fields`/`form_class`, and missing permission mixins.
2. Normalize the account/user flow: custom manager, signup form, profile routes, and template references.
3. Harden configuration: move secret/debug/hosts to environment variables, add `.env.example`, and improve `.gitignore`.
4. Extract cart/order/inventory mutations into explicit service functions and remove signal-driven side effects.
5. Migrate quantity fields from zero-decimal `DecimalField` to integer-based fields where safe.
6. Repair templates that still reference stale names or broken form actions.
7. Add focused tests for user creation, cart merge behavior, order creation, inventory rejection, and admin permission checks.
8. Finish with documentation cleanup (`README.md`, `docs/architecture.md`) and verification via `manage.py check` and test runs.

## Notes for this refactor

- The current SQLite data shows quantity values are whole numbers, so migrating cart/order quantity fields to integer-based fields is safe.
- The app should stay on SQLite/Django templates/classic views for this refactor; the issues are mostly correctness and maintainability, not stack choice.
