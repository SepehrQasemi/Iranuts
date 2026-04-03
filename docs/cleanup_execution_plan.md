# Cleanup Execution Plan

## Baseline

- Working repository: `C:\dev\Iranuts`
- Git remote:
  - `origin https://github.com/SepehrQasemi/Iranuts`
- Working branch:
  - `cleanup/portfolio-hardening`
- Audit baseline used:
  - `docs/audit/01_project_overview.md`
  - `docs/audit/02_architecture_map.md`
  - `docs/audit/03_data_model_report.md`
  - `docs/audit/04_user_flows.md`
  - `docs/audit/05_code_quality_and_risks.md`
  - `docs/audit/06_runtime_verification.md`
  - `docs/audit/07_portfolio_assessment.md`
  - `docs/audit/08_refactor_plan.md`
  - `docs/audit/09_evidence_index.md`
  - `docs/audit/10_executive_summary.md`

## Confirmed issues

These issues were reconfirmed against the real GitHub checkout before the cleanup port was finalized:

### Auth/profile

- dead `logedin` route and template baggage existed
- login/logout flow depended on fragile redirect templates
- profile ownership routes were not under clear `accounts` ownership
- phone-based login UX was not explicit

### Template/UI consistency

- templates were flat under `templates/`
- shared footer/navigation content was hardcoded
- hardcoded category IDs existed in `Base.html`
- encoding/text artifacts existed
- suspicious leftovers existed:
  - `templates/Users.html`
  - sparse `templates/InventoryView.html`

### Naming and domain drift

- `Order.is_send`
- `Post.summaries`
- awkward cart/order route names

### Order-history hardening

- `OrderItem` lacked immutable price snapshots

### Admin

- admin registration was mostly raw/default

### Tests

- the original repo did not have broad regression coverage for the most important flows

## Already-resolved issues

These are now implemented in the branch:

- auth/profile cleanup
- template namespacing and removal of suspicious leftovers
- naming cleanup for `is_send` and `summaries`
- immutable `OrderItem` pricing snapshots
- service-layer-backed order flow retained and hardened
- improved `ModelAdmin` classes
- expanded regression coverage

## Skipped issues

These were intentionally left unchanged:

- splitting the monolith into more Django apps
- changing SQLite to another database
- rewriting migration history
- redesigning the public URL scheme broadly just to make names prettier
- adding payment, shipment, or other fake commerce complexity
- replacing the cart-creation signal

## Risky areas

### Schema renames

- field renames required migration-backed updates across views, templates, admin, and tests

### Template relocation

- moving from flat templates to namespaced folders touched many render paths and reverse lookups

### Order mutation path

- adding `unit_price` and `line_total` changed a central business flow and therefore had to remain transactional and test-backed

### Legacy route compatibility

- account-owned routes were moved toward `accounts`, but legacy root profile URLs were preserved as redirects to avoid abrupt breakage

## Execution order

1. verify the GitHub repository and branch safely
2. port the audited cleanup into the real repository
3. finish auth/profile cleanup and route ownership
4. finish template/UI cleanup and remove leftovers
5. harden order history with price snapshots
6. improve admin usability
7. add the one-click local run workflow
8. expand tests and re-run verification
9. update README and final cleanup documentation
