# 09 Evidence Index

## Important files reviewed

| Path | Why it matters | Short note |
| --- | --- | --- |
| `config/settings.py` | Core runtime/config truth | Confirms env handling, SQLite, custom user, templates, static/media |
| `config/urls.py` | Root routing map | Shows how `Shop`, `accounts`, `blog`, and auth URLs are composed |
| `config/mixins.py` | Permission enforcement | Defines admin-only and owner-or-admin access checks |
| `manage.py` | Django entry point | Confirms standard project boot path |
| `requirements.txt` | Dependency truth | Small dependency set: Django and Pillow |

## Important models

| Path | Why it matters | Short note |
| --- | --- | --- |
| `accounts/models.py` | Identity and user-side effects | Custom phone-based auth model and cart-creation signal |
| `accounts/managers.py` | Auth correctness | Defines phone normalization and user/superuser creation |
| `Shop/models.py` | Main business domain | Contains catalog, inventory, cart, and order data model |
| `blog/models.py` | Peripheral content domain | Single `Post` model tied to the custom user |

## Important views

| Path | Why it matters | Short note |
| --- | --- | --- |
| `accounts/views.py` | Signup and profile flows | Handles signup, logged-in page, profile view/edit |
| `Shop/views.py` | Main behavior hub | Mixes storefront, admin CRUD, cart, order, and search logic |
| `Shop/services.py` | Critical business mutation logic | Handles cart merging and transactional order creation |
| `blog/views.py` | Blog public/admin flow | Simple list/detail plus admin CRUD |

## Important templates

| Path | Why it matters | Short note |
| --- | --- | --- |
| `templates/Base.html` | Shared UI shell | Navigation/footer hardcoding and text artifacts live here |
| `templates/ProductDetail.html` | Add-to-cart entry | POSTs product ID and quantity to cart endpoint |
| `templates/CartView.html` | Cart/order entry | Handles cart item update/delete and order creation form |
| `templates/Profile.html` | Profile display | Confirms user-profile rendering path |
| `templates/OrderView.html` | Admin order visibility | Shows what admins see for order management |
| `templates/registration/signup.html` | Signup UX | Renders custom user creation fields |
| `templates/registration/login.html` | Login UX | Uses Django auth form while semantically treating username as phone |
| `templates/registration/logedin.html` | Suspicious auth redirect | Depends on `localStorage.previousUrl` |
| `templates/registration/logged_out.html` | Suspicious auth redirect | Same redirect dependency as above |
| `templates/PostDetails.html` | Public blog detail | Includes edit/delete buttons in page UI |

## Important URLs

| Path | Why it matters | Short note |
| --- | --- | --- |
| `Shop/urls.py` | Main app routing | Catalog, supplier, inventory, cart, order, and profile routes |
| `accounts/urls.py` | Auth-specific routing | Only signup and custom logged-in page live here |
| `blog/urls.py` | Blog routing | Public blog list/detail and admin blog CRUD |

## Important migrations

| Path | Why it matters | Short note |
| --- | --- | --- |
| `accounts/migrations/0001_initial.py` | Early model history | Shows older user geography coupling |
| `accounts/migrations/0009_remove_customuser_province.py` | Drift signal | Confirms later removal of province from user |
| `Shop/migrations/0004_form.py` | Historical oddity | Temporary `Form` model with low-quality field naming |
| `Shop/migrations/0006_city_province_delete_form_city_province.py` | Domain shift | Deletes old form idea and introduces location models |
| `Shop/migrations/0010_rename_province_inventory_province_cartitem.py` | Important evolution | Renames inventory province field and introduces cart items |
| `Shop/migrations/0012_category_product_supplier_product_category.py` | Catalog growth | Adds category structure and earlier supplier linkage |
| `Shop/migrations/0021_refactor_cart_order_logic.py` | Recent stabilization | Signals newer work on cart/order correctness |
| `Shop/migrations/0023_alter_order_address_alter_order_province_and_more.py` | Current state alignment | Shows recent model hardening is already applied |

## Suspicious files

| Path | Why it matters | Short note |
| --- | --- | --- |
| `templates/Users.html` | Looks unused or placeholder-like | Does not match main system flows |
| `templates/InventoryView.html` | Looks incomplete | Sparse file compared with other view templates |
| `templates/registration/logedin.html` | Suspicious redirect logic | Depends on absent `previousUrl` write path |
| `templates/registration/logged_out.html` | Suspicious redirect logic | Same issue as above |
| `Iranuts/` | Empty top-level directory | Looks like an abandoned or placeholder app/package |

## Junk/local artifacts

| Path | Why it matters | Short note |
| --- | --- | --- |
| `db.sqlite3` | Local runtime state | Useful for local demo, but should not define repo quality |
| `media/` | Local upload state | Better treated as local/generated content for portfolio use |
| `.vscode/` | Editor-local config | Not core project architecture |
| `docs/refactor_audit.md` | Earlier workspace artifact | Indicates the repo was already being modified/documented before this audit |
| `docs/architecture.md` | Earlier workspace artifact | Another sign current workspace is not the untouched original snapshot |

## Runtime evidence

| Evidence source | Why it matters | Short note |
| --- | --- | --- |
| `python manage.py check` | Runtime sanity | Passed with no issues |
| `python manage.py showmigrations` | Schema state | All migrations applied |
| `python manage.py makemigrations --check` | Model/schema consistency | No pending changes |
| `python manage.py test` | Behavioral evidence | Current 5-test suite passes |
| SQLite table inspection | Demo-state evidence | Products/categories/inventory exist; suppliers/orders are sparse or empty |

## Interpretation note

This evidence index is intentionally biased toward files that support the audit’s main conclusions. It is not a full file inventory. Items are included because they materially influence:

- architecture understanding
- flow reconstruction
- risk assessment
- portfolio judgment
