from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Discount(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name="discounts",
        null=True,
        blank=True,
    )
    discount_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)



class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

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


# Signals to generate slug for Category, SubCategory, and Product
@receiver(pre_save, sender=Category)
@receiver(pre_save, sender=SubCategory)
@receiver(pre_save, sender=Product)
def generate_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
