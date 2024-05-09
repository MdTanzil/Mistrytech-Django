from rest_framework import serializers
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


class ImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Image
        exclude = [
            "created_at",
            "updated_at",
            "is_active",
            "product",
            "category",
            "subcategory",
            "url",
        ]


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        exclude = ["created_at", "updated_at", "is_active"]


class DiscountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Discount
        exclude = ["created_at", "updated_at", "is_active"]


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        exclude = ["created_at", "updated_at", "is_active"]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        exclude = ["created_at", "updated_at", "is_active"]


class CategoryDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            "url",
            "images",
            "products",
            "subcategories",
            "name",
            "description",
            "slug",
        ]


class CategoryListSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["url", "name", "description", "slug", "images"]


class VariantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Variant
        exclude = ["created_at", "updated_at", "is_active"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["url", "id", "username", "email", "password", "phone_number"]
        read_only_fields = ["id", "url"]


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        exclude = ["created_at", "updated_at", "is_active"]


class ShippingAddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShippingAddress
        exclude = ["created_at", "updated_at", "is_active"]


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ["created_at", "updated_at", "is_active"]


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payment
        exclude = ["created_at", "updated_at", "is_active"]



class SubCategoryDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = [
            "url",
            "images",
            "products",
            "name",
            "description",
            "slug",
        ]


class SubCategoryListSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ["url", "name", "description", "slug", "images"]
