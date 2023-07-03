from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver


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
    
    def __str__(self):
        return str(self.inventory.province.name + " " + self.product.name)


class Supplier(models.Model):
    name=models.CharField(max_length=50)
    Province=models.ForeignKey("Province", on_delete=models.CASCADE)
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
    quantity = models.DecimalField(max_digits=7, decimal_places=0)


    def save(self, *args, **kwargs):
        if not self.pk:  # Only execute this logic for newly created instances
            existing_instance = CartItem.objects.filter(product=self.product, cart=self.cart).first()
            if existing_instance:
                existing_instance.quantity += self.quantity
                existing_instance.save()
                return  # Exit early, no need to save the new instance
        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.product)

class Order(models.Model):
    user = models.ForeignKey('accounts.CustomUser',on_delete=models.CASCADE,default="")
    is_send=models.BooleanField(default=False)
    province=models.ForeignKey('Province',on_delete=models.CASCADE,default="")
    address=models.TextField(default="")
    def __str__(self):
        return str(self.user)

class OrderItem(models.Model):
    product = models.ForeignKey('Product',models.CASCADE)
    order = models.ForeignKey('Order',on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=9, decimal_places=0)

    def __str__(self):
        return str(self.product)

@receiver(post_save, sender=OrderItem)
def decrease_quantity_create(sender, instance, created, **kwargs):
    if created:
        product = Product.objects.filter(id=instance.product.id).first()
        inventoryProduct=InventoryProduct.objects.filter(product=product,inventory__province=instance.order.province).first()
        if product:
            inventoryProduct.quantity -= instance.quantity
            if inventoryProduct.quantity>=0:
                inventoryProduct.save()

            else:
                pass


@receiver(pre_save, sender=OrderItem)
def decrease_quantity_update(sender, instance, **kwargs):
    if instance.pk:
        # Retrieve the original instance of SecondModel from the database
        original_quantity = OrderItem.objects.get(pk=instance.pk)

        # Calculate the difference between the original count and the new count
        quantity_diff = original_quantity.quantity - instance.quantity
        # Update the count field of the first model
        product = Product.objects.get(id=instance.product.id)
        inventoryProduct = InventoryProduct.objects.filter(product=product, inventory__province=instance.order.province).first()
        if product:
            inventoryProduct.quantity+=quantity_diff
            if inventoryProduct.quantity >= 0:
                inventoryProduct.save()
            else:
                raise ValueError('Quantity of request is more than quantity of product')



@receiver(post_delete, sender=OrderItem)
def increase_count(sender, instance, **kwargs):
    product = Product.objects.filter(id=instance.product.id).first()
    inventoryProduct = InventoryProduct.objects.filter(product=product, inventory__province=instance.order.province).first()
    if product:
        inventoryProduct.quantity +=instance.quantity
        if inventoryProduct.quantity >= 0:
            inventoryProduct.save()
        else:
            raise ValueError('Quantity of request is more than quantity of product')