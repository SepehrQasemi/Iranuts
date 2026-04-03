# 08 Refactor Plan

## Refactor principles

- Preserve the domain:
  - products
  - categories
  - inventory
  - cart
  - orders
  - accounts
- Keep the Django monolith
- Prefer incremental, reviewable steps
- Keep the app runnable after each step
- Fix correctness before aesthetics
- Replace ambiguity with explicit code paths
- Do not rewrite migrations/history unless absolutely necessary

## Safe first steps

1. Freeze the current audited baseline.
2. Add or improve documentation so current behavior is explicit.
3. Run a browser smoke test and capture known-good screenshots.
4. Clean repository junk and local artifacts from public presentation.
5. Tidy the most obvious naming and template inconsistencies that do not require behavioral change.

## High-value low-risk fixes

- normalize obvious naming mistakes:
  - `logedin`
  - `is_send` if handled carefully through migration
  - `summaries` if handled carefully through migration
- make login/logout redirects explicit and conventional
- remove or confirm suspicious leftovers such as:
  - `templates/Users.html`
  - empty `Iranuts/`
- make footer/navigation category content dynamic
- replace hardcoded text/encoding issues in `Base.html`
- add tests for currently undercovered but important flows:
  - profile edit authorization
  - blog admin CRUD permissions
  - login/logout redirect behavior

## High-risk areas to treat carefully

### Order and inventory mutation

Why risky:

- touches the most important business correctness path
- affects stock levels and order creation

How to treat it:

- keep the service layer
- add tests before changing behavior
- avoid mixing new business rules with cleanup-only changes

### Custom user/auth behavior

Why risky:

- login identity depends on phone number
- cart creation depends on user creation

How to treat it:

- preserve the authentication contract
- document whether the signal remains or is replaced

### Data model renames

Why risky:

- field renames ripple into views, templates, forms, tests, admin, and migrations

How to treat it:

- group renames into deliberate migration-backed changes
- avoid bundling them with unrelated cleanup

## Suggested order of operations

### Phase 1: Truth and safety

- complete the audit baseline
- smoke-test the app in a browser
- identify any routes/templates that still fail at runtime

### Phase 2: Repository hygiene

- improve `.gitignore`
- remove local artifacts from source control posture
- remove clearly dead files after confirming no references

### Phase 3: Naming and structural cleanup

- normalize obvious route/template/view naming issues
- move account-related routing ownership toward `accounts`
- group templates by app without changing rendered behavior

### Phase 4: Business correctness hardening

- add immutable pricing to `OrderItem`
- decide whether to keep or replace the cart-creation signal
- harden validation around order address and province/inventory matching

### Phase 5: Admin and UX polish

- improve admin model configuration
- make admin pages more intentional than raw CRUD
- clean front-end presentation and base layout consistency

### Phase 6: Portfolio packaging

- finalize README
- add architecture docs and screenshots
- describe the project as a legacy cleanup case study

## Suggested test plan

### Expand automated tests around

- auth:
  - signup
  - login
  - logout redirect behavior
- profile:
  - owner vs non-owner access
- storefront:
  - product/category/search views return expected pages
- cart/order:
  - item update/delete
  - invalid quantity rejection
  - price snapshot if added
- admin:
  - supplier/inventory/blog write-path permissions

### Add one browser smoke checklist

- anonymous browse product/category/blog
- signup/login
- add product to cart
- update cart
- create order
- admin views inventory/order screens

## Suggested admin hardening plan

- register custom `ModelAdmin` classes for:
  - `Product`
  - `InventoryProduct`
  - `Order`
  - `Supplier`
- add useful list displays, search fields, and filters
- reduce accidental misuse of raw admin forms
- consider read-only fields where appropriate

## Suggested template/UI consistency plan

- group templates by app or concern
- standardize naming style
- remove hardcoded footer category IDs
- clean typography/text artifacts
- ensure auth pages share consistent navigation behavior
- keep the UI simple; do not overdesign the academic project into something artificial

## Suggested portfolio polish plan

- produce a clean README with:
  - overview
  - features
  - architecture
  - setup
  - screenshots
  - known limitations
- add 3 to 5 screenshots of:
  - product listing
  - product detail
  - cart/order flow
  - inventory admin page
- frame the project as:
  - reverse-engineered legacy Django cleanup
  - maintainability improvement exercise

## Do not touch first

- do not rewrite the whole app into APIs/frontend frameworks
- do not replace SQLite just for appearances
- do not split the monolith into many new apps before the current ones are clarified
- do not rewrite migration history
- do not redesign the domain before the current behavior is fully verified
- do not perform UI-only beautification before fixing correctness and consistency

## Bottom line

The right strategy is not reinvention. It is controlled recovery:

- understand
- verify
- clean
- harden
- document
- then polish
