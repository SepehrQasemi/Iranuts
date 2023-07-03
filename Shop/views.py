from typing import Any, Dict
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView ,TemplateView,CreateView,UpdateView,DeleteView,DetailView
from .models import *
from .froms import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin

class HomePage(TemplateView):
    template_name = 'HomePage.html'


class AboutUs(TemplateView):
    template_name = 'AboutUs.html'


class ContactUs(TemplateView):
    template_name = 'ContactUs.html'


class ProfileView(TemplateView):
    template_name='Profile.html'


class ProfileEdit(UpdateView):
    template_name='ProfileEdit.html'
    

class ProductView(ListView):
    model=Product
    template_name="ProductView.html"


class ProductCreate(CreateView):
    model=Product
    template_name='ProductCreate.html'
    def get_success_url(self):
        return reverse_lazy('ProductDetail',args=(self.object.id,))
    def test_func(self):
        return self.request.user.is_superuser


class ProductEdit(UpdateView):
    model=Product
    template_name='ProductEdit.html'
    def get_success_url(self):
        return reverse_lazy('ProductDetail',args=(self.object.id,))
    def test_func(self):
        return self.request.user.is_superuser


class ProductDelete(DeleteView):
    model = Product
    template_name='ProductDelete.html'
    success_url = reverse_lazy('ProductView')
    def test_func(self):
        return self.request.user.is_superuser


class ProductDetail(DetailView):
    model=Product
    template_name='ProductDetail.html'
    context_object_name = 'Product'


class CategoryView(ListView):
    model = Category
    template_name = 'CategoryView.html'


class CategoryDetail(DetailView):
    model = Category
    template_name = 'CategoryDetail.html'
    

class CategoryCreate(CreateView):
    model = Category
    template_name = 'CategoryCreate.html'
    fields = '__all__'
    def get_success_url(self):
        return reverse_lazy('CategoryDetail',args=(self.object.id,))
    def test_func(self):
        return self.request.user.is_superuser


class CategoryEdit(UpdateView):
    model = Category
    template_name = 'CategoryEdit.html'
    fields = '__all__'
    def get_success_url(self):
        return reverse_lazy('CategoryDetail',args=(self.object.id,))
    def test_func(self):
        return self.request.user.is_superuser
    

class CategoryDelete(DeleteView):
    model = Category
    template_name = 'CategoryDelete.html'
    success_url = reverse_lazy('CategoryView')
    def test_func(self):
        return self.request.user.is_superuser


class SupplierView(ListView):
    model = Category
    template_name = 'SupplierView.html'


class SupplierCreate(CreateView):
    model=Supplier
    template_name='SupplierCreate.html'
    def get_success_url(self):
        return reverse_lazy('SupplierDetail',args=(self.object.id,))
    def test_func(self):
        return self.request.user.is_superuser


class SupplierEdit(UpdateView):
    model=Supplier
    template_name='SupplierEdit.html'
    def get_success_url(self):
        return reverse_lazy('SupplierDetail',args=(self.object.id,))
    def test_func(self):
        return self.request.user.is_superuser


class SupplierDelete(DeleteView):
    model=Supplier
    template_name='SupplierDelete.html'
    success_url = reverse_lazy('SupplierView')
    def test_func(self):
        return self.request.user.is_superuser


class SupplierDetail(DetailView):
    model=Supplier
    template_name='SupplierDetail.html'


class InventoryView(ListView):
    model = Inventory
    template_name = 'InventoryView.html'


class InventoryCreate(CreateView):
    model=Inventory
    template_name='InventoryCreate.html'
    def get_success_url(self):
        return reverse_lazy('InventoryDetail',args=(self.object.id,))
    def test_func(self):
        return self.request.user.is_superuser


class InventoryEdit(UpdateView):
    model=Inventory
    template_name='InventoryEdit.html'
    def get_success_url(self):
        return reverse_lazy('InventoryDetail',args=(self.object.id,))


class InventoryDelete(DeleteView):
    model=Inventory
    template_name='InventoryDelete.html'
    success_url = reverse_lazy('InventoryView')
    def test_func(self):
        return self.request.user.is_superuser


class InventoryDetail(DetailView):
    model=Inventory
    template_name='InventoryDetail.html'



    
class Search (TemplateView):
    template_name="Search.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Search=self.request.GET.get('search')
        
        try:
            context['products'] = Product.objects.filter(name__contains=Search)
        except:
            pass

        try:
            context['Category'] = Category.objects.filter(name__contains=Search)
        except:
            pass

    
        return context


class InventoryProductView(UserPassesTestMixin,ListView):
    model = InventoryProduct
    template_name = 'InventoryProduct.html'

    def test_func(self):
        return self.request.user.is_superuser


class InventoryProductDetail(UserPassesTestMixin,DetailView):
    model = InventoryProduct
    template_name = 'InventoryProductDetail.html'

    def test_func(self):
        return self.request.user.is_superuser


class InventoryProductCreate(UserPassesTestMixin,CreateView):
    model = InventoryProduct
    template_name = 'InventoryProductCreate.html'
    def get_success_url(self):
        return reverse_lazy('InventoryProductDetail',args=(self.object.id,))
    def test_func(self):
        return self.request.user.is_superuser
    

class InventoryProductEdit(UserPassesTestMixin,UpdateView):
    model = InventoryProduct
    template_name = 'InventoryProductCreate.html'
    def get_success_url(self):
        return reverse_lazy('InventoryProductDetail',args=(self.object.id,))

    def test_func(self):
        return self.request.user.is_superuser
    

class InventoryProductDelete(UserPassesTestMixin,DeleteView):
    model = InventoryProduct
    template_name = 'InventoryProductDelete.html'
    success_url = reverse_lazy('InventoryProduct')
    def test_func(self):
        return self.request.user.is_superuser

class CartDetailView(UserPassesTestMixin,DetailView):
    model = Cart
    template_name = 'CartView.html'
    
    def get_context_data(self, **kwargs):
        context=super(CartDetailView, self).get_context_data()
        totalPrice=0
        for cartItem in context['cart'].cartitem_set.all():
            totalPrice+=cartItem.quantity*cartItem.product.price
        context['totalprice']=totalPrice
        province=Province.objects.filter(inventory__in=Inventory.objects.all())
        context['province']=province
        return context
    def test_func(self):
        return self.request.user==self.get_object().user



def addToCart(request):
    if request.method=='POST':
        cart=Cart.objects.get(user=request.user)
        cartItem=CartItem(cart=cart,product_id=request.POST.get('Product'),quantity=int(request.POST.get('quantity')))
        cartItem.save()
        return redirect(request.META['HTTP_REFERER'])

def updateCart(request,cartItemId):
    
    if request.method=='POST':
        cartItem=CartItem.objects.get(id=cartItemId,cart__user=request.user)
        cartItem.quantity=float(request.POST.get('quantity'))
        cartItem.save()
        return redirect(request.META['HTTP_REFERER'])


def deletFromCart(request,cartItemId):
    if request.method=='POST':
        cartItem=CartItem.objects.get(id=cartItemId,cart__user=request.user)
        cartItem.delete()
        return redirect(request.META['HTTP_REFERER'])

class OrderView(UserPassesTestMixin,ListView):
    model = Order
    template_name = 'OrderView.html'
    def test_func(self):
        return self.request.user.is_superuser


def orderCreate(request):
    if request.method=="POST":
        order=Order(user=request.user , province_id=request.POST.get('orderprovince'),address=request.POST.get('orderaddress'))
        items = []
        x=True
        province=Province.objects.get(id=request.POST.get('orderprovince'))
        for idItem in tuple(dict(request.POST).values())[3:]:
            cartitem=CartItem.objects.get(id=int(idItem[0]))
            product=cartitem.product
            if product.inventoryproduct_set.filter(inventory__province=province):
                inventoryProduct=product.inventoryproduct_set.get(inventory__province=province)
                if inventoryProduct.quantity>cartitem.quantity:
                    items.append(OrderItem(product=product,order=order,quantity=cartitem.quantity))

                else:
                    x=False
                    messages.error(request,f'{product.name}:Your request is more than our quantity')

            else:
                x=False
                messages.error(request,f'{product.name}:This product is not available in your province')

        if x:
            order.save()
            for item in items:
                item.save()
            Cart.objects.get(user=request.user).delete()
            Cart(user=request.user).save()
            return redirect('HomePage')
        return redirect('CartView',request.user.cart.id)



class OrderListVeiw(UserPassesTestMixin,ListView):
    model = Order
    template_name = 'orders.html'
    def test_func(self):
        return self.request.user.is_superuser

class OrderUpdate(UserPassesTestMixin,UpdateView):
    model = Order
    template_name = 'orderupdate.html'
    fields = ['is_send']
    success_url = reverse_lazy('orders')
    def test_func(self):
        return self.request.user.is_superuser

