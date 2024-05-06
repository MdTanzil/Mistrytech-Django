from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from .models import Category, SubCategory, Discount, Product, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0  # Set to 0 to remove the empty extra row


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "subcategory",
        "price",
        "quantity",
        "image_display",
        "is_active",
    )
    list_filter = ("category", "subcategory", "is_active")
    search_fields = ["name", "description"]
    inlines = [
        ImageInline
    ]  # Include ImageInline to display images related to the product
    list_per_page = 20  # Number of items per page
    ordering = ('-id',)  # Sort by ID in descending order

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

    image_display.short_description = "Images"  # Changed to plural 'Images'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "image_display", "is_active")
    list_filter = ("is_active",)
    search_fields = ["name", "description"]
    inlines = [
        ImageInline
    ] 
    list_per_page = 20  # Number of items per page
    ordering = ('-id',)  # Sort by ID in descending order

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
    inlines = [
        ImageInline
    ] 
    list_per_page = 20  # Number of items per page
    ordering = ('-id',)  # Sort by ID in descending order


class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "discount_value",
        "description",
        "start_date",
        "end_date",
        "is_active",
    )
    list_filter = ("is_active",'end_date','start_date')
    search_fields = ["product__name", "description",'end_date','start_date']
    list_per_page = 20  # Number of items per page
    ordering = ('-id',)  # Sort by ID in descending order


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Product, ProductAdmin)
