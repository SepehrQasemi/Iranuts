from django.db import migrations, models


def deduplicate_cart_items(apps, schema_editor):
    CartItem = apps.get_model("Shop", "CartItem")
    seen = {}

    for item in CartItem.objects.all().order_by("cart_id", "product_id", "id"):
        if item.quantity <= 0:
            item.delete()
            continue

        key = (item.cart_id, item.product_id)
        if key in seen:
            primary = seen[key]
            primary.quantity += item.quantity
            primary.save(update_fields=["quantity"])
            item.delete()
        else:
            seen[key] = item


def deduplicate_order_items(apps, schema_editor):
    OrderItem = apps.get_model("Shop", "OrderItem")
    seen = {}

    for item in OrderItem.objects.all().order_by("order_id", "product_id", "id"):
        if item.quantity <= 0:
            item.delete()
            continue

        key = (item.order_id, item.product_id)
        if key in seen:
            primary = seen[key]
            primary.quantity += item.quantity
            primary.save(update_fields=["quantity"])
            item.delete()
        else:
            seen[key] = item


class Migration(migrations.Migration):
    dependencies = [
        ("Shop", "0020_order_address_order_is_send_order_province_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="supplier",
            old_name="Province",
            new_name="province",
        ),
        migrations.RunPython(deduplicate_cart_items, migrations.RunPython.noop),
        migrations.RunPython(deduplicate_order_items, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="cartitem",
            name="quantity",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="quantity",
            field=models.PositiveIntegerField(),
        ),
        migrations.AddConstraint(
            model_name="inventoryproduct",
            constraint=models.UniqueConstraint(fields=("inventory", "product"), name="unique_inventory_product"),
        ),
        migrations.AddConstraint(
            model_name="cartitem",
            constraint=models.UniqueConstraint(fields=("cart", "product"), name="unique_cart_product"),
        ),
        migrations.AddConstraint(
            model_name="cartitem",
            constraint=models.CheckConstraint(check=models.Q(quantity__gt=0), name="cart_item_quantity_gt_zero"),
        ),
        migrations.AddConstraint(
            model_name="orderitem",
            constraint=models.UniqueConstraint(fields=("order", "product"), name="unique_order_product"),
        ),
        migrations.AddConstraint(
            model_name="orderitem",
            constraint=models.CheckConstraint(check=models.Q(quantity__gt=0), name="order_item_quantity_gt_zero"),
        ),
    ]
