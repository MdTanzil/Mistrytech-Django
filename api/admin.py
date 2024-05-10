from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from .models import (
    Category,
    SubCategory,
    Discount,
    Product,
    Image,
    Variant,
    User,
    Order,
    ShippingAddress,
    OrderItem,
    Payment,
)
from django.contrib.auth.admin import UserAdmin


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0  # Set to 0 to remove the empty extra row


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Set to 0 to remove the empty extra row

class VariantInline(admin.TabularInline):
    model = Variant
    extra = 0  # Set to 0 to remove the empty extra row




class ShippingAddressInline(admin.TabularInline):
    model = ShippingAddress
    extra = 0  # Set to 0 to remove the empty extra row


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0  # Set to 0 to remove the empty extra row


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_categories",
        "get_subcategories",
        "price",
        "discounted_price",
        "quantity",
        "image_display",
        "is_active",
    )
    list_filter = ("category", "subcategory", "is_active")
    search_fields = ["name", "description"]
    inlines = [
        VariantInline,
        ImageInline
    ]  # Include ImageInline to display images related to the product
    list_per_page = 20  # Number of items per page
    ordering = ("-id",)  # Sort by ID in descending order
    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.category.all()])
    def get_subcategories(self, obj):
        return ", ".join([subcategory.name for subcategory in obj.subcategory.all()])
    def discounted_price(self, obj):
        return obj.discounted_price
    get_categories.short_description = 'Categories'
    get_subcategories.short_description = 'Subcategories'
    def image_display(self, obj):
        images_html = ""
        if (
            obj.images.exists()
        ):  # Assuming 'images' is the related_name for the Image model
            for image in obj.images.all():
                images_html += (
                    f'<img src="{image.image.url}" width="40" height="40" />&nbsp;'
                )
        else:
            images_html = "No Images"
        return mark_safe(images_html)

    image_display.short_description = "Images"  # Changed to plural 'Images'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "image_display", "is_active")
    list_filter = ("is_active",)
    search_fields = ["name", "description"]
    inlines = [ImageInline]
    list_per_page = 20  # Number of items per page
    ordering = ("-id",)  # Sort by ID in descending order

    def image_display(self, obj):
        images_html = ""
        if (
            obj.images.exists()
        ):  # Assuming 'images' is the related_name for the Image model
            for image in obj.images.all():
                images_html += (
                    f'<img src="{image.image.url}" width="50" height="50" />&nbsp;'
                )
        else:
            images_html = "No Images"
        return mark_safe(images_html)

    image_display.short_description = "Images"


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "description", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ["name", "description"]
    inlines = [ImageInline]
    list_per_page = 20  # Number of items per page
    ordering = ("-id",)  # Sort by ID in descending order


class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        "discount_value",
        "description",
        "start_date",
        "end_date",
        "is_active",
    )
    list_filter = ("is_active", "end_date", "start_date", "product")
    search_fields = ["description", "end_date", "start_date"]
    list_per_page = 20  # Number of items per page
    ordering = ("-id",)  # Sort by ID in descending order


class VariantAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "discount",
        "size",
        "price",
        "quantity",
        "is_active",
    )
    list_filter = ("is_active", "product")
    # search_fields = ['end_date','start_date']
    list_per_page = 20  # Number of items per page
    ordering = ("-id",)  # Sort by ID in descending order


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "phone_number", "is_staff")
    # Add phone_number to fieldsets and add_fieldsets
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "phone_number")},
        ),  # Include phone_number here
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    inlines = [OrderItemInline, ShippingAddressInline, PaymentInline]
    search_fields = ["id"]
    ordering = ("-id",)
    list_per_page = 20


class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "variant",
        "price",
        "quantity",
    )
    list_filter = ("is_active", "product")
    search_fields = ["id", "order"]
    list_per_page = 20  # Number of items per page
    ordering = ("-id",)  # Sort by ID in descending order


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "payment_method",
        "payment_status",
        "amount",
        "transaction_id",
    )
    search_fields = ["transaction_id", "id"]
    list_filter = ("is_active",)
    # search_fields = ['end_date','start_date']
    list_per_page = 20  # Number of items per page
    ordering = ("-id",)  # Sort by ID in descending order


class ImageAdmin(admin.ModelAdmin):
    search_fields = ["id"]
    ordering = ("-id",)
    list_per_page = 20


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(ShippingAddress)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
