from django.contrib import admin
from decimal import Decimal

from .models import Cart, CartItem, Category, Inventory, InventoryProduct, Order, OrderItem, Product, Province, Supplier


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "product_count")
    search_fields = ("name",)

    @admin.display(description="Products")
    def product_count(self, obj):
        return obj.product_set.count()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "inventory_locations")
    search_fields = ("name", "description", "category__name")
    list_filter = ("category",)

    @admin.display(description="Inventories")
    def inventory_locations(self, obj):
        return obj.inventoryproduct_set.count()


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("province", "phone")
    search_fields = ("province__name", "address", "phone")
    list_filter = ("province",)


@admin.register(InventoryProduct)
class InventoryProductAdmin(admin.ModelAdmin):
    list_display = ("product", "inventory", "province_name", "quantity")
    search_fields = ("product__name", "inventory__province__name")
    list_filter = ("inventory__province",)

    @admin.display(description="Province")
    def province_name(self, obj):
        return obj.inventory.province.name


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "province", "phone", "email")
    search_fields = ("name", "phone", "email", "address")
    list_filter = ("province",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    search_fields = ("user__phone", "user__first_name", "user__last_name")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")
    search_fields = ("cart__user__phone", "product__name")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    fields = ("product", "quantity", "unit_price", "line_total")
    readonly_fields = fields


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "province", "is_sent", "item_count", "order_total")
    search_fields = ("user__phone", "user__first_name", "user__last_name", "address")
    list_filter = ("is_sent", "province")
    readonly_fields = ("user", "province", "address", "order_total")
    fields = ("user", "province", "address", "is_sent", "order_total")
    inlines = [OrderItemInline]

    @admin.display(description="Items")
    def item_count(self, obj):
        return obj.orderitem_set.count()

    @admin.display(description="Total")
    def order_total(self, obj):
        return sum((item.line_total for item in obj.orderitem_set.all()), Decimal("0.00"))


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "unit_price", "line_total")
    search_fields = ("order__user__phone", "product__name")
    readonly_fields = ("order", "product", "quantity", "unit_price", "line_total")
