from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ShopIndexView,
    GroupListView,
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDetailView,
    ProductDeleteView,
    OrderListView,
    OrderDetailView,
    ProductsDataExportView,
    ProductViewSet,
)

app_name = 'shopapp'

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns =  [
    path('', ShopIndexView.as_view(), name='index'),
    # path('api/', include(router.urls)),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/update', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/archive/', ProductDeleteView.as_view(), name='product-delete'),
    path('groups/', GroupListView.as_view(), name='grou ps-list'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('api/products/export/', ProductsDataExportView.as_view(), name='products-export'),

]


urlpatterns += router.urls