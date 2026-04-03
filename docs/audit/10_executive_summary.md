# 10 Executive Summary

## What this project is

`Iranuts-main` is a Django monolith that appears to implement a small storefront and back-office management system. Its main domain is:

- products and categories
- province-based inventory
- carts and orders
- customer accounts using phone-based login
- a small blog/content section

This is not a toy “single-model CRUD” project. It has a real domain and several connected workflows, which gives it meaningful educational and portfolio value.

## What state it is in now

The current workspace is not a pristine untouched 3-year-old repository. It already contains newer stabilization work, including:

- a service layer for cart/order logic
- a small test suite
- `.env`-style configuration support
- newer documentation and migrations

That matters because the audit describes the project as it exists today, while still identifying older legacy drift and design residue.

## Whether it still works

What was verified:

- dependencies install
- Django system checks pass
- migrations are applied
- current models match migration state
- the current 5-test suite passes
- the main flows can be traced clearly in code

What was not fully verified:

- full browser-based end-to-end interaction across all pages
- all template render paths
- login/logout redirect behavior involving custom `logedin` and `logged_out` templates
- real operational use of supplier management and some admin screens

So the honest answer is:

- the project appears runnable in its current audited state
- it is partially runtime-verified
- it is not fully end-to-end verified

## Biggest risks

### 1. Uneven maturity

The main business path is more careful than the surrounding project, but the rest of the codebase still shows student-project roughness:

- mixed naming
- flat template structure
- hardcoded UI content
- leftover files/artifacts

### 2. Thin order model

`OrderItem` does not capture immutable sale price data. If product prices change later, historical order meaning becomes weaker. This is one of the most important business-model weaknesses.

### 3. Hidden side effects

New users automatically receive carts through a post-save signal. That works, but it hides behavior that should be easy to reason about in a legacy codebase.

### 4. Overloaded view layer

`Shop/views.py` still carries too many responsibilities:

- storefront pages
- admin CRUD
- search
- cart behavior
- order behavior

This is the main maintainability bottleneck.

### 5. Presentation quality

The project is structurally better than it looks. Right now, the UI/template layer makes it appear less mature than the underlying domain deserves.

## Whether it is worth saving

Yes, but not as-is.

This project is worth saving because:

- the domain is coherent
- the app has enough complexity to be interesting
- the current runtime posture is better than many abandoned student projects
- it can be framed as a legacy rescue / maintainability improvement case study

It is not a “light polish and publish immediately” project.

The right verdict is:

- worth a serious cleanup

## What should happen next

Recommended next step:

1. Treat this audit as the baseline truth.
2. Do one browser-level smoke test of the main flows.
3. Clean the most visible quality problems first:
   - template inconsistency
   - naming mistakes
   - hardcoded footer/nav content
   - leftover junk files/artifacts
4. Harden the business model where it matters most:
   - order item price snapshot
   - explicit auth redirect behavior
   - clearer ownership of account routes
5. Then package the project as a portfolio-ready Django monolith recovery project.

## Bottom line

This repository should not be discarded, and it should not be presented publicly in its current form.

It is a salvageable legacy academic Django project with a credible retail/inventory domain, partial modern cleanup already in place, and enough substance to justify a structured improvement pass. The strongest public narrative is not “look at my perfect old project.” It is:

- “I reverse-engineered an old Django codebase, audited it honestly, stabilized the core flows, and turned it into a maintainable portfolio project.”
