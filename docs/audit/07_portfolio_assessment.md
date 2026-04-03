# 07 Portfolio Assessment

## Current strengths

- The project has a real domain, not a toy CRUD theme.
- It combines customer-facing and admin-facing workflows.
- The core model set is understandable and commercially plausible.
- The current workspace has a cleaner transaction path than many student Django projects because cart/order logic now lives in a service layer.
- Django checks pass and the current small test suite passes.
- The stack is simple and credible:
  - Django
  - SQLite
  - server-rendered templates

## Current weaknesses

- Presentation quality is still visibly student-project level.
- Naming inconsistencies weaken trust immediately.
- The template layer is flat and inconsistent.
- Some UX flows are crude or suspicious, especially login/logout redirection.
- The order model is too thin for serious commerce credibility.
- Historical drift and leftover artifacts are visible in the repository.
- The admin side works more like raw CRUD scaffolding than a carefully designed back-office tool.

## What makes it salvageable

This project is salvageable because its core is not nonsense.

What is worth keeping:

- coherent product/category/cart/order domain
- custom user model with a clear identity choice
- province-based inventory design
- recent transactional service extraction
- small dependency footprint

What would make it unsalvageable is not present:

- no evidence of total architectural chaos
- no evidence of a broken data model beyond normal student-project limitations
- no evidence of impossible-to-understand business purpose

## What makes it risky for portfolio use right now

- the repository still contains signs of unfinished cleanup
- some code and template names read as careless rather than deliberate
- UI hardcoding and text/encoding issues make the project look less professional than it needs to
- a reviewer could quickly notice that order history is not modeled robustly

## Best way to describe it on a portfolio / GitHub README

Best framing:

- “Legacy Django e-commerce/inventory project cleaned up into a maintainable monolith”
- “Server-rendered Django storefront with custom phone-based auth, province-based inventory, cart/order workflow, and admin management”

This framing works because it turns the project into a maintenance/recovery story rather than pretending it was originally polished.

## What to hide or de-emphasize

- raw screenshots of the current UI before cleanup
- migration-history oddities
- unfinished or leftover templates/files
- any claim that it is production-grade commerce software

## What must be improved before showing it publicly

- template and UI consistency
- naming cleanup for obviously awkward terms
- removal of junk/local artifacts from the repository presentation
- at least one browser-verified smoke-tested demo path
- stronger order-history modeling or, at minimum, honest documentation of the limitation
- clearer README and architecture notes

## Final verdict

### Verdict

`worth a serious cleanup`

### Why

The project is too substantial to discard and too uneven to present as-is.

If the goal is portfolio value, this is not a “light polish and publish” case. It needs a deliberate cleanup focused on:

- clarity
- consistency
- confidence in the main flows
- better presentation of the system’s strengths

## Direct recommendation

Do not abandon it.

Do not showcase it in its current form either.

Treat it as a legacy rescue project:

- keep the current domain and monolith structure
- stabilize and document the main flows
- remove visible sloppiness
- tighten a few core business rules
- present it as an example of reverse-engineering and improving an existing Django codebase

That is the strongest portfolio narrative available for this repository.
