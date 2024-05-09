from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.hashers import make_password
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .serializers import (
    CategorySerializer,
    SubCategorySerializer,
    DiscountSerializer,
    ProductSerializer,
    ImageSerializer,
    VariantSerializer,
    UserSerializer,
    OrderSerializer,
    ShippingAddressSerializer,
    OrderItemSerializer,
    PaymentSerializer,
    CategoryDetailSerializer,
    CategoryListSerializer,
    SubCategoryDetailSerializer,
    SubCategoryListSerializer
    )
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
from rest_framework.response import Response  # Import Response
from rest_framework.decorators import action 


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        validated_data["password"] = make_password(validated_data["password"])
        serializer.save()

    def perform_update(self, serializer):
        validated_data = serializer.validated_data
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        serializer.save()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, url_path='products')
    def get_category_products(self, request, pk=None):
        category = self.get_object()
        products = Product.objects.filter(subcategory__category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    

class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
class ShippingAddressViewSet(viewsets.ModelViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    

class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class SubCategoryDetailView(RetrieveAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryDetailSerializer

class SubCategoryListView(ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryListSerializer