from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Cart, CartItem, InventoryProduct, Order, OrderItem


def normalize_quantity(raw_quantity):
    try:
        quantity = int(raw_quantity)
    except (TypeError, ValueError) as exc:
        raise ValidationError("Quantity must be a valid whole number.") from exc

    if quantity <= 0:
        raise ValidationError("Quantity must be greater than zero.")

    return quantity


@transaction.atomic
def add_product_to_cart(*, user, product, quantity):
    normalized_quantity = normalize_quantity(quantity)
    cart, _ = Cart.objects.get_or_create(user=user)

    cart_item = CartItem.objects.select_for_update().filter(cart=cart, product=product).first()
    if cart_item:
        cart_item.quantity += normalized_quantity
        cart_item.save(update_fields=["quantity"])
        return cart_item

    return CartItem.objects.create(cart=cart, product=product, quantity=normalized_quantity)


@transaction.atomic
def update_cart_item_quantity(*, cart_item, quantity):
    cart_item.quantity = normalize_quantity(quantity)
    cart_item.save(update_fields=["quantity"])
    return cart_item


@transaction.atomic
def create_order_from_cart(*, user, province, address, cart_item_ids):
    cart = Cart.objects.select_for_update().get(user=user)
    cart_items = list(
        CartItem.objects.select_for_update()
        .filter(cart=cart, id__in=cart_item_ids)
        .select_related("product")
    )

    if not cart_items:
        raise ValidationError("Your cart is empty.")

    inventory_products = {}
    errors = []

    for cart_item in cart_items:
        inventory_product = InventoryProduct.objects.select_for_update().filter(
            product=cart_item.product,
            inventory__province=province,
        ).first()

        if not inventory_product:
            errors.append(f"{cart_item.product.name}: This product is not available in your province.")
            continue

        if inventory_product.quantity < cart_item.quantity:
            errors.append(f"{cart_item.product.name}: Your request is more than our quantity.")
            continue

        inventory_products[cart_item.id] = inventory_product

    if errors:
        raise ValidationError(errors)

    order = Order.objects.create(user=user, province=province, address=address)
    OrderItem.objects.bulk_create(
        [
            OrderItem(
                product=cart_item.product,
                order=order,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price,
                line_total=cart_item.product.price * cart_item.quantity,
            )
            for cart_item in cart_items
        ]
    )

    for cart_item in cart_items:
        inventory_product = inventory_products[cart_item.id]
        inventory_product.quantity -= cart_item.quantity
        inventory_product.save(update_fields=["quantity"])

    cart.cartitem_set.filter(id__in=cart_item_ids).delete()
    return order
