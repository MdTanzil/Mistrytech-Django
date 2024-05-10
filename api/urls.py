from django.urls import path, include
from rest_framework import routers
from .views import (
    UserViewSet,
    CategoryViewSet,
    SubCategoryViewSet,
    DiscountViewSet,
    ProductViewSet,
    ImageViewSet,
    VariantViewSet,
    OrderViewSet,
    PaymentViewSet,
    CategoryDetailView,
    CategoryListView,
    SubCategoryDetailView,
    SubCategoryListView,
    SubCategoryDetailViewSlag,
    CategoryDetailViewSlag,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
# router.register(r"category", CategoryViewSet)
# router.register(r"subcategory", SubCategoryViewSet)
router.register(r"discount", DiscountViewSet)
router.register(r"product", ProductViewSet)
router.register(r"image", ImageViewSet)
router.register(r"variant", VariantViewSet)
router.register(r"order", OrderViewSet)
router.register(r"payment", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("category/", CategoryListView.as_view(), name="category-list"),
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("subcategory/", SubCategoryListView.as_view(), name="subcategory-list"),
    path(
        "category/slug/<slug:slug>/",
        CategoryDetailViewSlag.as_view(),
        name="category-detail",
    ),
    path(
        "subcategory/<int:pk>/",
        SubCategoryDetailView.as_view(),
        name="subcategory-detail",
    ),
    path(
        "subcategory/slug/<slug:slug>/",
        SubCategoryDetailViewSlag.as_view(),
        name="subcategory-detail-slug",
    ),
]
