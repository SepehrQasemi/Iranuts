from django import forms

from .models import Category, Inventory, InventoryProduct, Product, Supplier


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class ProductForm(BootstrapModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class CategoryForm(BootstrapModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class SupplierForm(BootstrapModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"


class InventoryForm(BootstrapModelForm):
    class Meta:
        model = Inventory
        fields = "__all__"


class InventoryProductForm(BootstrapModelForm):
    class Meta:
        model = InventoryProduct
        fields = "__all__"
