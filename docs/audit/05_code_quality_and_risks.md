# 05 Code Quality And Risks

## Reading stance

This section is intentionally critical. It focuses on evidence-based problems, not on preserving optimism.

## Naming problems

### Issue: mixed and awkward naming across routes, fields, and templates

- Severity: `medium`
- Evidence:
  - `/accounts/logedin/`
  - `Order.is_send`
  - `Post.summaries`
  - flat template names such as `ProductView.html`, `PostDetails.html`, `Profile.html`
- Why it matters:
  - increases relearning cost
  - signals uneven design standards
  - makes the codebase look more academic and less polished
- Suggested fix direction:
  - normalize route names, template naming, and awkward model field names in a controlled migration/refactor pass

## Broken conventions

### Issue: profile routes live in `Shop/urls.py` instead of `accounts/urls.py`

- Severity: `medium`
- Evidence:
  - profile views are defined in `accounts/views.py`
  - profile URLs are mounted in `Shop/urls.py`
- Why it matters:
  - breaks app ownership expectations
  - makes navigation logic harder to re-discover
- Suggested fix direction:
  - move or re-namespace account-owned routes during a later cleanup pass

### Issue: inconsistent app boundaries

- Severity: `medium`
- Evidence:
  - `accounts` creates `Shop.Cart` via signal
  - `blog` depends on the custom user model
  - `Shop` is both storefront and admin back office
- Why it matters:
  - stronger coupling reduces maintainability
  - future refactors become riskier
- Suggested fix direction:
  - keep the monolith, but make boundaries more explicit through services and clearer ownership

## Incomplete or suspicious views

### Issue: custom logged-in / logged-out flow looks incomplete

- Severity: `medium`
- Evidence:
  - `templates/registration/logedin.html`
  - `templates/registration/logged_out.html`
  - both rely on `localStorage.previousUrl`
  - no code was found that sets `previousUrl`
- Why it matters:
  - user redirection behavior may be broken or inconsistent
- Suggested fix direction:
  - replace this with standard Django auth redirect settings or explicitly implement the missing write path

### Issue: blog create flow exposes all model fields

- Severity: `medium`
- Evidence:
  - `blog.views.PostCreate` uses `fields = "__all__"`
- Why it matters:
  - admin users can edit fields more broadly than necessary
  - the create workflow is less intentional than it should be
- Suggested fix direction:
  - use a dedicated form or explicit fields and set `author` from the request when appropriate

## Template inconsistencies

### Issue: flat template layout with mixed naming and mixed concerns

- Severity: `medium`
- Evidence:
  - most templates are under top-level `templates/`
  - app-specific templates are not strongly namespaced
- Why it matters:
  - makes template discovery slower
  - increases the chance of accidental name collisions
- Suggested fix direction:
  - move toward app namespaces without changing user behavior

### Issue: hardcoded UI content in the base template

- Severity: `medium`
- Evidence:
  - `templates/Base.html` contains hardcoded category links to IDs `1`, `2`, `3`
  - hardcoded contact/location content
  - encoding artifact `Â© 2023`
- Why it matters:
  - UI is brittle
  - content is not data-driven
  - portfolio impression is weaker
- Suggested fix direction:
  - make footer/nav category listings dynamic and clean the text encoding

### Issue: suspicious leftover templates

- Severity: `low`
- Evidence:
  - `templates/Users.html`
  - `templates/InventoryView.html` appears suspiciously sparse
- Why it matters:
  - leftover files reduce trust in the repository
- Suggested fix direction:
  - confirm whether these are used; remove or replace if not

## Dead code / junk files / probable leftovers

### Issue: repository contains local/runtime artifacts

- Severity: `medium`
- Evidence:
  - `db.sqlite3`
  - `media/`
  - `.vscode/`
- Why it matters:
  - muddies repository cleanliness
  - can leak local state into portfolio presentation
- Suggested fix direction:
  - exclude local artifacts from public/source control workflows unless explicitly needed

### Issue: empty or suspicious directories/files remain

- Severity: `low`
- Evidence:
  - empty `Iranuts/` directory
  - migration residue such as old `Form` model history
- Why it matters:
  - suggests poor cleanup discipline
- Suggested fix direction:
  - document and prune dead assets after confirming no runtime dependency

## Dangerous patterns

### Issue: hidden cart creation side effect via signal

- Severity: `high`
- Evidence:
  - `accounts.models` post-save signal creates `Shop.Cart`
- Why it matters:
  - signals make business behavior implicit
  - debugging user creation becomes less obvious
  - repeated signal expansion is a common source of legacy Django surprises
- Suggested fix direction:
  - either keep it and document it clearly, or replace it with an explicit service during controlled refactor work

### Issue: order history does not snapshot sale price

- Severity: `high`
- Evidence:
  - `Shop.OrderItem` stores only `product` and `quantity`
  - no per-line unit price or subtotal field exists
- Why it matters:
  - historical order data can become inaccurate if product prices later change
  - weakens domain credibility for a commerce project
- Suggested fix direction:
  - add immutable price capture on order creation before using this publicly

### Issue: admin CRUD directly edits stock without an audit model

- Severity: `medium`
- Evidence:
  - inventory is modified through raw generic CRUD views on `InventoryProduct`
- Why it matters:
  - stock changes are operationally sensitive
  - there is no adjustment log or reason tracking
- Suggested fix direction:
  - if this project is polished, add a minimal stock-adjustment pattern or at least stricter admin conventions

## Hidden side effects

### Issue: business logic is split across services, views, and signals

- Severity: `medium`
- Evidence:
  - `Shop/services.py` handles core order/cart logic
  - `Shop/views.py` still contains important request-level validation/selection logic
  - `accounts.models` signal creates carts
- Why it matters:
  - the current design is better than older fat-view logic, but still not conceptually clean
- Suggested fix direction:
  - consolidate critical domain mutations into explicit services and document those entry points

## Validation weaknesses

### Issue: form/model validation is uneven

- Severity: `medium`
- Evidence:
  - many admin CRUD forms use `fields = "__all__"` or `fields = "__all__"`-style forms
  - order address handling is minimal
  - login UX still depends on a username-named field for phone login
- Why it matters:
  - inconsistent validation creates edge-case risk
- Suggested fix direction:
  - add explicit form validation where the business meaning matters

## Permission/security weaknesses

### Issue: local-dev settings are acceptable, but production posture remains thin

- Severity: `medium`
- Evidence:
  - `.env`-driven settings exist
  - SQLite is the only configured database
  - media serving is handled in Django URL configuration
- Why it matters:
  - current setup is good for local development, not for strong deployment posture
- Suggested fix direction:
  - keep local simplicity, but separate “portfolio/demo ready” from “production ready” in documentation

### Issue: admin checks rely on `is_superuser` only

- Severity: `low`
- Evidence:
  - `config.mixins.AdminRequiredMixin`
- Why it matters:
  - works for a small app, but is coarse-grained
- Suggested fix direction:
  - acceptable for now; consider staff/permission granularity only if the project grows

## Maintainability issues

### Issue: `Shop/views.py` is still the most overloaded file

- Severity: `high`
- Evidence:
  - contains storefront pages, admin CRUD, search, cart, and order behavior
- Why it matters:
  - this is the main relearning bottleneck
  - future edits have high collision risk
- Suggested fix direction:
  - split by concern in later phases without changing behavior

### Issue: historical drift is visible in migration history and file layout

- Severity: `medium`
- Evidence:
  - migrations show renamed/deleted concepts
  - the repo contains old residue and newer stabilization work side by side
- Why it matters:
  - makes it harder to separate “original design” from “current truth”
- Suggested fix direction:
  - document current architecture clearly and avoid rewriting migration history

## Testing gaps

### Issue: test coverage exists, but it is narrow and recent-looking

- Severity: `medium`
- Evidence:
  - current tests cover:
    - custom user creation
    - cart item merge
    - order creation success
    - insufficient inventory rejection
    - admin page permissions
- Why it matters:
  - many flows remain untested:
    - login/logout redirection
    - profile editing behavior
    - supplier CRUD
    - blog CRUD
    - template rendering consistency
- Suggested fix direction:
  - expand tests around auth UX, inventory admin flows, and regression-prone templates

## Deployment/configuration issues

### Issue: current startup path was not fully browser-verified

- Severity: `medium`
- Evidence:
  - `manage.py check` passes
  - tests pass
  - runserver attempts timed out without complete interaction verification
- Why it matters:
  - passing checks do not prove end-to-end page rendering
- Suggested fix direction:
  - do one browser-level smoke test before presenting the project publicly

## Overall quality assessment

### What is better than expected

- the domain is coherent
- recent service extraction improved the riskiest transaction path
- system checks and current tests pass

### What still looks amateur or legacy-bound

- naming consistency
- template organization
- UI hardcoding
- leftover artifacts
- weak order-history modeling
- overloaded views

## Bottom line

This is not a disaster, but it is not clean enough to present without further work. The project’s biggest problem is uneven maturity: parts of it are now reasonable, while surrounding code and presentation still advertise legacy/student-project quality.
