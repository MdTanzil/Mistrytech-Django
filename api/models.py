from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from decimal import Decimal
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )
    bannerImage = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return (
            f"{self.name } | {self.category.name if self.category else 'No category'}"
        )


class Discount(models.Model):
    discount_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.discount_value}% discount"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    category = models.ManyToManyField(
        Category,
        related_name="products_in_category",
        blank=True,
    )
    subcategory = models.ManyToManyField(
        SubCategory,
        related_name="products_in_subcategory",
        blank=True,
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
        related_name="product",
        null=True,
        blank=True,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @property
    def discounted_price(self):
        if self.discount:
            discount_value = self.discount.discount_value
            if discount_value is not None:
                discount_amount = self.price * (discount_value / Decimal(100))
                discounted_price = self.price - discount_amount
                return discounted_price
        return self.price

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", null=True, blank=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="images", null=True, blank=True
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Image id #{self.id}"


class Variant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
        null=True,
        blank=True,
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
        related_name="variants",
        null=True,
        blank=True,
    )
    image = models.ImageField(null=True, blank=True)
    size = models.FloatField(null=True, blank=True)
    color = models.CharField(null=True, blank=True,max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @property
    def discounted_price(self):
        if self.discount:
            discount_value = self.discount.discount_value
            if discount_value is not None:
                discount_amount = self.price * (discount_value / Decimal(100))
                discounted_price = self.price - discount_amount
                return discounted_price
        return self.price

    def __str__(self):
        return f"Variant of {self.product.name if self.product else 'price'}"


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username


class Order(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, related_name="orders", on_delete=models.SET_NULL
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    gross_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    shipping_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    net_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Order Id #{self.id}"


class ShippingAddress(models.Model):
    order = models.OneToOneField(
        Order,
        null=True,
        blank=True,
        related_name="shipping_address",
        on_delete=models.CASCADE,
    )
    full_address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return self.full_address


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        null=True,
        blank=True,
        related_name="order_items",
        on_delete=models.SET_NULL,
    )
    variant = models.ForeignKey(
        Variant,
        null=True,
        blank=True,
        related_name="order_items",
        on_delete=models.SET_NULL,
    )
    quantity = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Id : ' {self.id}' Product quantity{self.quantity} product price{self.price}"


class Payment(models.Model):
    order = models.ForeignKey(
        Order, null=True, blank=True, related_name="payments", on_delete=models.CASCADE
    )
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.CharField(max_length=100, null=True, blank=True)
    amount = models.FloatField()
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.payment_status


class ContractForm(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    phone= models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    massage = models.TextField( blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

# Signals to generate slug for Category, SubCategory, and Product
@receiver(pre_save, sender=Category)
@receiver(pre_save, sender=SubCategory)
@receiver(pre_save, sender=Product)
def generate_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
