from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.



class User(AbstractUser):
    id = models.AutoField(primary_key=True)       #
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=15, unique=True)
    first_name =models.CharField(max_length=100)
    last_name =models.CharField(max_length=100)
    password = models.CharField(max_length=255)   # store hashed passwords
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True, max_length=150)
    image = models.ImageField(upload_to='images/category', blank=True, null=True)

    def __str__(self):
        return self.name


def short_uuid():
    return uuid.uuid4().hex[:12]

class Product(models.Model):
    link = models.CharField(unique=True,max_length=12 , default=short_uuid)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='product/images', blank=True, null=True)
    description = models.TextField()
    date_saved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    session_key = models.CharField(max_length=40, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.first_name

class CartItem(models.Model):
    cart_id =  models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.name

class Order(models.Model):
    order_number = models.CharField(max_length=20,  editable=False)
    user_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15 )
    address = models.CharField(max_length=250)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, )

    def save(self, *args, **kwargs):
        if not self.order_number:
            with transaction.atomic():
                last = Order.objects.select_for_update().order_by('-order_number').first()
                self.order_number = 1 if not last else int(last.order_number) + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.order_number)


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.order_id