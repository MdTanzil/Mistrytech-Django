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

class DiscountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Discount
        exclude = ["created_at", "updated_at", "is_active"]

class VariantSerializer(serializers.HyperlinkedModelSerializer):
    discount= DiscountSerializer(many=False,read_only=True)
    class Meta:
        model = Variant
        exclude = ["created_at", "updated_at", "is_active"]
        extra_kwargs = {
            'id': {'read_only': False},  # Make 'id' field writable
        }

class SubCategorySerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        exclude = ["created_at", "updated_at", "is_active"]




class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    variants = VariantSerializer(many=True,read_only=True)
    discount= DiscountSerializer(many=False,read_only=True)

    class Meta:
        model = Product
        exclude = ["created_at", "updated_at", "is_active",'category','subcategory']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        exclude = ["created_at", "updated_at", "is_active"]


class CategoryDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True,source='products_in_category')
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
    products = ProductSerializer(many=True, read_only=True,source='products_in_subcategory')
    class Meta:
        model = SubCategory
        fields = [
            "url",
            "images",
            "products",
            "name",
            "description",
            "slug",
            'id'
        ]


class SubCategoryListSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ["url", "name", "description", "slug", "images"]
