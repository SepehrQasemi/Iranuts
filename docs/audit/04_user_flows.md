# 04 User Flows

## Method

This report reconstructs flows from code by tracing:

- URL pattern
- view
- form or request parsing
- models touched
- template rendering
- side effects

Confidence labels:

- `verified`: code path and supporting template/model evidence are clear, and runtime checks do not contradict it
- `partially verified`: the code path is clear, but full browser/runtime confirmation was not completed
- `unverified`: path exists, but behavior could not be confidently established from the current evidence

## Signup / login / logout

### Entry points

- Signup:
  - URL: `/accounts/signup/`
  - View: `accounts.views.SignUpView`
  - Form: `accounts.forms.SignUpForm`
  - Template: `templates/registration/signup.html`
- Login:
  - URL: `/accounts/login/`
  - View: Django built-in auth view
  - Template: `templates/registration/login.html`
- Logout:
  - URL: `/accounts/logout/`
  - View: Django built-in auth view
  - Templates:
    - `templates/registration/logout.html`
    - `templates/registration/logged_out.html`
- Custom “logged in” page:
  - URL: `/accounts/logedin/`
  - View: `accounts.views.LoggedInView`
  - Template: `templates/registration/logedin.html`

### Code path

- Signup uses `UserCreationForm` on `CustomUser`
- user creation goes through `CustomUserManager.create_user`
- `accounts.models` post-save signal auto-creates a `Shop.Cart`
- login uses Django auth against `USERNAME_FIELD = "phone"`

### Models touched

- `accounts.CustomUser`
- `Shop.Cart` via signal

### Side effects

- creating a user automatically creates a cart

### Permissions/auth assumptions

- signup is public
- login/logout use Django auth conventions

### Likely failure points

- login UX is slightly nonstandard because the form field is still `username` but semantically means phone number
- custom pages `logedin` / `logged_out` use JavaScript redirects based on `localStorage.previousUrl`
- no code was found that writes `previousUrl`, so the redirect behavior looks incomplete

### Confidence level

- `partially verified`

## Profile viewing/editing

### Entry points

- View profile:
  - URL: `/Profile/<pk>/`
  - View: `accounts.views.ProfileView`
  - Template: `templates/Profile.html`
- Edit profile:
  - URL: `/ProfileEdit/<pk>/`
  - View: `accounts.views.ProfileEdit`
  - Template: `templates/ProfileEdit.html`

### Code path

- routes are declared in `Shop/urls.py`
- views live in `accounts/views.py`
- `UserOwnsObjectOrAdminMixin` restricts access

### Models touched

- `accounts.CustomUser`

### Side effects

- edit flow updates user fields directly through a generic `UpdateView`

### Permissions/auth assumptions

- user can edit only their own profile unless superuser

### Likely failure points

- route ownership is architecturally confusing because profile URLs are in `Shop/urls.py`
- profile templates are flat and not app-namespaced

### Confidence level

- `verified`

## Browsing products/categories

### Entry points

- Products:
  - `/ProductView/`
  - `/ProductDetail/<pk>/`
- Categories:
  - `/CategoryView/`
  - `/CategoryDetail/<pk>/`
- Search:
  - `/Search/`

### Code path

- class-based list/detail views in `Shop/views.py`
- templates:
  - `ProductView.html`
  - `ProductDetail.html`
  - `CategoryView.html`
  - `CategoryDetail.html`
  - `Search.html`

### Models touched

- `Shop.Product`
- `Shop.Category`

### Side effects

- none beyond rendering

### Permissions/auth assumptions

- public

### Likely failure points

- navigation/footer content is partly hardcoded in `Base.html`
- category footer links point to fixed numeric IDs rather than dynamic data
- search is simple `icontains` matching with no pagination or normalization

### Confidence level

- `verified`

## Adding to cart

### Entry points

- POST `/addtocart/`
- product detail form in `templates/ProductDetail.html`

### Code path

- `Shop.views.add_to_cart`
- delegates to `Shop.services.add_product_to_cart`
- redirects back to `HTTP_REFERER`

### Models touched

- `Shop.Cart`
- `Shop.CartItem`
- `Shop.Product`

### Side effects

- creates cart if missing
- merges quantities when the same product already exists in the cart

### Permissions/auth assumptions

- `@login_required`

### Likely failure points

- `HTTP_REFERER` is not guaranteed by clients
- if referer is absent, redirect behavior could degrade
- quantity validation depends on posted form values and service-layer checks

### Confidence level

- `verified`

## Updating/removing cart items

### Entry points

- Update:
  - POST `/CartEdit/<cart_item_id>/`
  - form in `templates/CartView.html`
- Delete:
  - POST `/CartDelete/<cart_item_id>/`
  - form in `templates/CartView.html`
- View cart:
  - `/Cart/<pk>/`

### Code path

- `Shop.views.CartDetailView`
- `Shop.views.update_cart`
- `Shop.views.delete_from_cart`
- update path uses `Shop.services.update_cart_item_quantity`

### Models touched

- `Shop.Cart`
- `Shop.CartItem`

### Side effects

- updating to a nonpositive quantity deletes the item
- delete endpoint removes the line item

### Permissions/auth assumptions

- cart detail requires login and ownership check
- update/delete endpoints explicitly compare `cart_item.cart.user` to `request.user`

### Likely failure points

- cart item IDs are posted directly and rely on object-level owner checks
- there is no optimistic locking or stale-cart protection

### Confidence level

- `verified`

## Creating an order

### Entry points

- POST `/OrderCreate/`
- form embedded in `templates/CartView.html`

### Code path

- `Shop.views.create_order`
- extracts selected cart item IDs, province ID, and address from POST
- delegates to `Shop.services.create_order_from_cart`

### Models touched

- `Shop.Cart`
- `Shop.CartItem`
- `Shop.Order`
- `Shop.OrderItem`
- `Shop.InventoryProduct`
- `Shop.Province`

### Side effects

- validates requested province
- validates stock availability for selected items
- creates order and order-item rows
- decrements matching inventory rows
- deletes purchased cart items
- wraps the mutation in a database transaction

### Permissions/auth assumptions

- `@login_required`

### Likely failure points

- order creation depends on the selected province having matching inventory rows
- no payment step exists
- no total-price snapshot exists on order or order items
- address handling is thin and not strongly validated

### Confidence level

- `verified`

## Inventory adjustments

### Entry points

- `/InventoryView/`
- `/InventoryCreate/`
- `/InventoryEdit/<pk>/`
- `/InventoryDelete/<pk>/`
- `/InventoryProduct/`
- `/InventoryProductCreate/`
- `/InventoryProductEdit/<pk>/`
- `/InventoryProductDelete/<pk>/`

### Code path

- admin-only generic views in `Shop/views.py`
- forms from `Shop/forms.py`

### Models touched

- `Shop.Inventory`
- `Shop.InventoryProduct`
- `Shop.Province`
- `Shop.Product`

### Side effects

- direct CRUD against stock records

### Permissions/auth assumptions

- guarded by `AdminRequiredMixin`

### Likely failure points

- admin CRUD exposes raw inventory mutation without a stronger audit trail
- no explicit service layer is used for manual stock edits
- `InventoryView.html` looked suspicious/incomplete in the template layer, though current route wiring exists

### Confidence level

- `partially verified`

## Supplier management

### Entry points

- `/SupplierView/`
- `/SupplierCreate/`
- `/SupplierEdit/<pk>/`
- `/SupplierDelete/<pk>/`
- `/SupplierDetail/<pk>/`

### Code path

- generic list/create/update/delete/detail views in `Shop/views.py`
- forms from `Shop/forms.py`
- templates:
  - `SupplierView.html`
  - `SupplierCreate.html`
  - `SupplierEdit.html`
  - `SupplierDelete.html`
  - `SupplierDetail.html`

### Models touched

- `Shop.Supplier`
- `Shop.Province`

### Side effects

- CRUD only

### Permissions/auth assumptions

- admin-only

### Likely failure points

- supplier data appears disconnected from the order/inventory workflow
- current database had zero suppliers at audit time, so real usage is unproven

### Confidence level

- `partially verified`

## Blog CRUD/display

### Entry points

- Public:
  - `/blog/`
  - `/blog/Post/<pk>`
- Admin:
  - `/new_post/`
  - `/PostEdit/<pk>/`
  - `/PostDelete/<pk>/`

### Code path

- `blog.views.PostView`
- `blog.views.PostDetails`
- `blog.views.PostCreate`
- `blog.views.PostEdit`
- `blog.views.PostDelete`

### Models touched

- `blog.Post`
- `accounts.CustomUser` through `author`

### Side effects

- admin CRUD mutates blog posts

### Permissions/auth assumptions

- public read
- admin-only write paths

### Likely failure points

- create form exposes all fields via `fields = "__all__"`
- there is no workflow to auto-assign author from `request.user`
- edit/delete buttons appear on the public post detail page, which is workable but not elegant

### Confidence level

- `partially verified`

## Cross-flow observations

### Where permissions are strongest

- profile object ownership
- admin-only inventory/supplier/order/blog write pages
- cart ownership checks

### Where the design is weakest

- redirect flow after login/logout
- hardcoded UI/navigation elements
- operational thinness of the order model
- dependence on a cart-creation signal

### Practical conclusion

The main storefront flow is understandable and currently more trustworthy than the surrounding presentation layer. The project’s biggest risk is not that the domain is incoherent; it is that the implementation quality varies sharply between newer logic and older surrounding code.
