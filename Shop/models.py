from django.db import models
from django.core.validators import RegexValidator


class Product(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=12,decimal_places=2)
    inventory = models.ManyToManyField("Inventory",through='InventoryProduct')
    image = models.ImageField()
    category=models.ForeignKey('Category',on_delete=models.CASCADE)
    # supplier=models.ManyToManyField('Supplier')
    def __str__(self):
        return self.name


class Province(models.Model):
    name=models.CharField(max_length=50)
    

    def __str__(self):
        return self.name



class Inventory(models.Model):
    province = models.OneToOneField("Province", on_delete=models.CASCADE)
    address = models.TextField(null=True,blank=True,)
    phone = models.CharField(null=True,blank=True,max_length=13,validators=[
        RegexValidator(
            
        regex=r'^\+?1?\d{11,11}$',
        message="Phone number must be in the format: '0999999999'. Up to 11 digits allowed."
        )
    ])
    def __str__(self):
        return str(self.province.name)


class InventoryProduct(models.Model):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey("Product",on_delete=models.CASCADE)
    
    inventory = models.ForeignKey("Inventory",on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["inventory", "product"], name="unique_inventory_product"),
        ]
    
    def __str__(self):
        return str(self.inventory.province.name + " " + self.product.name)


class Supplier(models.Model):
    name=models.CharField(max_length=50)
    province=models.ForeignKey("Province", on_delete=models.CASCADE)
    phone = models.CharField(null=False,blank=False,max_length=13,validators=[
        RegexValidator(
            
        regex=r'^\+?1?\d{11,11}$',
        message='Phone number must be like 09371889805'
        )
    ])
    email = models.EmailField(max_length=254)
    address = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField()
    def __str__(self):
        return self.name


class Cart(models.Model):
    user=models.OneToOneField('accounts.CustomUser' , on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)

class CartItem(models.Model):
    product=models.ForeignKey('Product' , on_delete=models.CASCADE)
    cart=models.ForeignKey('Cart',on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["cart", "product"], name="unique_cart_product"),
            models.CheckConstraint(check=models.Q(quantity__gt=0), name="cart_item_quantity_gt_zero"),
        ]


    def __str__(self):
        return str(self.product)

class Order(models.Model):
    user = models.ForeignKey('accounts.CustomUser',on_delete=models.CASCADE)
    is_sent=models.BooleanField(default=False)
    province=models.ForeignKey('Province',on_delete=models.CASCADE)
    address=models.TextField(blank=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.user.phone}"

class OrderItem(models.Model):
    product = models.ForeignKey('Product',models.CASCADE)
    order = models.ForeignKey('Order',on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["order", "product"], name="unique_order_product"),
            models.CheckConstraint(check=models.Q(quantity__gt=0), name="order_item_quantity_gt_zero"),
        ]

    def __str__(self):
        return f"{self.product} x {self.quantity}"
