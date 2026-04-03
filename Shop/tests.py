from decimal import Decimal
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import CustomUser

from .models import CartItem, Category, Inventory, InventoryProduct, Order, Product, Province
from .services import add_product_to_cart


def make_test_image(name):
    return SimpleUploadedFile(
        name,
        (
            b"GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,"
            b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
        ),
        content_type="image/gif",
    )


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class ShopWorkflowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._media_root = tempfile.mkdtemp()
        cls._media_override = override_settings(MEDIA_ROOT=cls._media_root)
        cls._media_override.enable()

    @classmethod
    def tearDownClass(cls):
        cls._media_override.disable()
        shutil.rmtree(cls._media_root, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.password = "StrongPass123!"
        self.user = CustomUser.objects.create_user(phone="09123456789", password=self.password)
        self.other_user = CustomUser.objects.create_user(phone="09123456788", password=self.password)
        self.admin = CustomUser.objects.create_superuser(phone="09999999999", password=self.password)
        self.category = Category.objects.create(name="Pistachio", image=make_test_image("category.gif"))
        self.product = Product.objects.create(
            name="Akbari Pistachio",
            description="Premium pistachio",
            price=Decimal("12.50"),
            image=make_test_image("product.gif"),
            category=self.category,
        )
        self.province = Province.objects.create(name="Tehran")
        self.inventory = Inventory.objects.create(province=self.province, address="Test address", phone="09111111111")
        self.inventory_product = InventoryProduct.objects.create(
            inventory=self.inventory,
            product=self.product,
            quantity=10,
        )

    def test_storefront_pages_render(self):
        urls = [
            reverse("HomePage"),
            reverse("ProductView"),
            reverse("ProductDetail", args=[self.product.id]),
            reverse("CategoryView"),
            reverse("CategoryDetail", args=[self.category.id]),
            reverse("Search") + "?search=Pistachio",
        ]

        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_add_to_cart_view_merges_items(self):
        self.client.force_login(self.user)

        self.client.post(
            reverse("add_to_cart"),
            {"product_id": self.product.id, "quantity": 1},
            HTTP_REFERER=reverse("ProductDetail", args=[self.product.id]),
        )
        self.client.post(
            reverse("add_to_cart"),
            {"product_id": self.product.id, "quantity": 2},
            HTTP_REFERER=reverse("ProductDetail", args=[self.product.id]),
        )

        cart_items = CartItem.objects.filter(cart=self.user.cart, product=self.product)
        self.assertEqual(cart_items.count(), 1)
        self.assertEqual(cart_items.get().quantity, 3)

    def test_cart_update_and_delete_views(self):
        add_product_to_cart(user=self.user, product=self.product, quantity=2)
        cart_item = self.user.cart.cartitem_set.get(product=self.product)
        self.client.force_login(self.user)

        update_response = self.client.post(
            reverse("cart_update", args=[cart_item.id]),
            {"quantity": 5},
            HTTP_REFERER=reverse("cart_detail", args=[self.user.cart.id]),
        )
        self.assertRedirects(update_response, reverse("cart_detail", args=[self.user.cart.id]))
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)

        delete_response = self.client.post(
            reverse("cart_delete", args=[cart_item.id]),
            HTTP_REFERER=reverse("cart_detail", args=[self.user.cart.id]),
        )
        self.assertRedirects(delete_response, reverse("cart_detail", args=[self.user.cart.id]))
        self.assertFalse(self.user.cart.cartitem_set.exists())

    def test_cart_detail_is_owner_only(self):
        self.client.force_login(self.other_user)
        response = self.client.get(reverse("cart_detail", args=[self.user.cart.id]))
        self.assertEqual(response.status_code, 403)

    def test_order_creation_success_records_price_snapshot(self):
        add_product_to_cart(user=self.user, product=self.product, quantity=2)
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("order_create"),
            {
                "province_id": self.province.id,
                "address": "123 Test Street",
                "cart_item_ids": list(self.user.cart.cartitem_set.values_list("id", flat=True)),
            },
            HTTP_REFERER=reverse("cart_detail", args=[self.user.cart.id]),
        )

        self.assertRedirects(response, reverse("HomePage"))
        order = Order.objects.get(user=self.user)
        order_item = order.orderitem_set.get()
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.unit_price, Decimal("12.50"))
        self.assertEqual(order_item.line_total, Decimal("25.00"))

        self.product.price = Decimal("19.99")
        self.product.save(update_fields=["price"])
        order_item.refresh_from_db()
        self.assertEqual(order_item.unit_price, Decimal("12.50"))
        self.assertEqual(order_item.line_total, Decimal("25.00"))

        self.inventory_product.refresh_from_db()
        self.assertEqual(self.inventory_product.quantity, 8)
        self.assertFalse(self.user.cart.cartitem_set.exists())

    def test_insufficient_inventory_rejection_keeps_cart_and_stock(self):
        add_product_to_cart(user=self.user, product=self.product, quantity=11)
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("order_create"),
            {
                "province_id": self.province.id,
                "address": "123 Test Street",
                "cart_item_ids": list(self.user.cart.cartitem_set.values_list("id", flat=True)),
            },
            HTTP_REFERER=reverse("cart_detail", args=[self.user.cart.id]),
        )

        self.assertRedirects(response, reverse("cart_detail", args=[self.user.cart.id]))
        self.assertEqual(Order.objects.count(), 0)
        self.inventory_product.refresh_from_db()
        self.assertEqual(self.inventory_product.quantity, 10)
        self.assertTrue(self.user.cart.cartitem_set.exists())

    def test_admin_only_pages_reject_regular_users(self):
        self.client.force_login(self.user)

        for url in [reverse("ProductCreate"), reverse("InventoryCreate"), reverse("SupplierView"), reverse("order_list")]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 403)

        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse("ProductCreate")).status_code, 200)
