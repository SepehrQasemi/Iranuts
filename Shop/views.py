"""Main storefront and back-office views for the Shop app."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from config.mixins import AdminRequiredMixin

from .forms import CategoryForm, InventoryForm, InventoryProductForm, ProductForm, SupplierForm
from .models import Cart, CartItem, Category, Inventory, InventoryProduct, Order, Product, Province, Supplier
from .services import add_product_to_cart, create_order_from_cart, update_cart_item_quantity


def _redirect_back(request, fallback):
    return redirect(request.META.get("HTTP_REFERER") or fallback)


def _flash_validation_error(request, exc):
    for error_message in exc.messages:
        messages.error(request, error_message)


class HomePage(TemplateView):
    template_name = 'shared/home.html'


class AboutUs(TemplateView):
    template_name = 'shared/about.html'


class ContactUs(TemplateView):
    template_name = 'shared/contact.html'


class ProductView(ListView):
    model = Product
    template_name = "shop/product_list.html"


class ProductCreate(AdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_create.html'

    def get_success_url(self):
        return reverse_lazy('ProductDetail', args=(self.object.id,))


class ProductEdit(AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_edit.html'
    context_object_name = 'product'

    def get_success_url(self):
        return reverse_lazy('ProductDetail', args=(self.object.id,))


class ProductDelete(AdminRequiredMixin, DeleteView):
    model = Product
    template_name = 'shop/product_delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('ProductView')


class ProductDetail(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'


class CategoryView(ListView):
    model = Category
    template_name = 'shop/category_list.html'


class CategoryDetail(DetailView):
    model = Category
    template_name = 'shop/category_detail.html'


class CategoryCreate(AdminRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'shop/category_create.html'

    def get_success_url(self):
        return reverse_lazy('CategoryDetail', args=(self.object.id,))


class CategoryEdit(AdminRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'shop/category_edit.html'
    context_object_name = 'category'

    def get_success_url(self):
        return reverse_lazy('CategoryDetail', args=(self.object.id,))


class CategoryDelete(AdminRequiredMixin, DeleteView):
    model = Category
    template_name = 'shop/category_delete.html'
    context_object_name = 'category'
    success_url = reverse_lazy('CategoryView')


class SupplierView(AdminRequiredMixin, ListView):
    model = Supplier
    template_name = 'shop/supplier_list.html'


class SupplierCreate(AdminRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'shop/supplier_create.html'

    def get_success_url(self):
        return reverse_lazy('SupplierDetail', args=(self.object.id,))


class SupplierEdit(AdminRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'shop/supplier_edit.html'
    context_object_name = 'supplier'

    def get_success_url(self):
        return reverse_lazy('SupplierDetail', args=(self.object.id,))


class SupplierDelete(AdminRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'shop/supplier_delete.html'
    context_object_name = 'supplier'
    success_url = reverse_lazy('SupplierView')


class SupplierDetail(AdminRequiredMixin, DetailView):
    model = Supplier
    template_name = 'shop/supplier_detail.html'
    context_object_name = 'supplier'


class InventoryView(AdminRequiredMixin, ListView):
    model = Inventory
    template_name = 'shop/inventory_list.html'


class InventoryCreate(AdminRequiredMixin, CreateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'shop/inventory_create.html'

    def get_success_url(self):
        return reverse_lazy('InventoryDetail', args=(self.object.id,))


class InventoryEdit(AdminRequiredMixin, UpdateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'shop/inventory_edit.html'
    context_object_name = 'inventory'

    def get_success_url(self):
        return reverse_lazy('InventoryDetail', args=(self.object.id,))


class InventoryDelete(AdminRequiredMixin, DeleteView):
    model = Inventory
    template_name = 'shop/inventory_delete.html'
    context_object_name = 'inventory'
    success_url = reverse_lazy('InventoryView')


class InventoryDetail(AdminRequiredMixin, DetailView):
    model = Inventory
    template_name = 'shop/inventory_detail.html'
    context_object_name = 'inventory'


class SearchView(TemplateView):
    template_name = "shop/search_results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search', '').strip()
        context['query'] = query
        context['products'] = Product.objects.filter(name__icontains=query) if query else Product.objects.none()
        context['categories'] = Category.objects.filter(name__icontains=query) if query else Category.objects.none()
        return context


class InventoryProductView(AdminRequiredMixin, ListView):
    model = InventoryProduct
    template_name = 'shop/inventory_product_list.html'


class InventoryProductDetail(AdminRequiredMixin, DetailView):
    model = InventoryProduct
    template_name = 'shop/inventory_product_detail.html'
    context_object_name = 'inventoryproduct'


class InventoryProductCreate(AdminRequiredMixin, CreateView):
    model = InventoryProduct
    form_class = InventoryProductForm
    template_name = 'shop/inventory_product_create.html'

    def get_success_url(self):
        return reverse_lazy('InventoryProductDetail', args=(self.object.id,))


class InventoryProductEdit(AdminRequiredMixin, UpdateView):
    model = InventoryProduct
    form_class = InventoryProductForm
    template_name = 'shop/inventory_product_edit.html'
    context_object_name = 'inventoryproduct'

    def get_success_url(self):
        return reverse_lazy('InventoryProductDetail', args=(self.object.id,))


class InventoryProductDelete(AdminRequiredMixin, DeleteView):
    model = InventoryProduct
    template_name = 'shop/inventory_product_delete.html'
    context_object_name = 'inventoryproduct'
    success_url = reverse_lazy('InventoryProduct')


class CartDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Cart
    template_name = 'shop/cart_detail.html'
    context_object_name = 'cart'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context['cart'].cartitem_set.select_related('product')
        context['totalprice'] = sum(cart_item.quantity * cart_item.product.price for cart_item in cart_items)
        context['provinces'] = Province.objects.filter(inventory__isnull=False).distinct()
        return context

    def test_func(self):
        return self.request.user == self.get_object().user


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product = get_object_or_404(
            Product,
            id=request.POST.get('product_id') or request.POST.get('Product'),
        )
        try:
            add_product_to_cart(
                user=request.user,
                product=product,
                quantity=request.POST.get('quantity', 0),
            )
        except ValidationError as exc:
            _flash_validation_error(request, exc)
    return _redirect_back(request, 'HomePage')


@login_required
def update_cart(request, cart_item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        try:
            quantity = int(request.POST.get('quantity', 0))
        except (TypeError, ValueError):
            messages.error(request, 'Quantity must be a valid whole number.')
            return _redirect_back(request, 'HomePage')

        if quantity <= 0:
            cart_item.delete()
        else:
            try:
                update_cart_item_quantity(cart_item=cart_item, quantity=quantity)
            except ValidationError as exc:
                _flash_validation_error(request, exc)
    return _redirect_back(request, 'HomePage')


@login_required
def delete_from_cart(request, cart_item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        cart_item.delete()
    return _redirect_back(request, 'HomePage')


@login_required
def create_order(request):
    if request.method == "POST":
        province_id = request.POST.get('province_id') or request.POST.get('orderprovince')
        if not province_id:
            messages.error(request, 'Please choose a province before ordering.')
            return redirect('cart_detail', request.user.cart.id)

        province = get_object_or_404(Province, id=province_id)
        address = request.POST.get('address') or request.POST.get('orderaddress', '')
        cart_item_ids = request.POST.getlist('cart_item_ids') or request.POST.getlist('cartitem_ids')
        try:
            create_order_from_cart(
                user=request.user,
                province=province,
                address=address,
                cart_item_ids=cart_item_ids,
            )
            messages.success(request, 'Your order was created successfully.')
            return redirect('HomePage')
        except ValidationError as exc:
            _flash_validation_error(request, exc)

    return redirect('cart_detail', request.user.cart.id)


class OrderListView(AdminRequiredMixin, ListView):
    model = Order
    template_name = 'shop/order_list.html'


class OrderUpdate(AdminRequiredMixin, UpdateView):
    model = Order
    template_name = 'shop/order_update.html'
    fields = ['is_sent']
    context_object_name = 'order'
    success_url = reverse_lazy('order_list')
