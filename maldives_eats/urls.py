from django.urls import path
from . import views

app_name = 'maldives_eats'

urlpatterns = [
    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Product URLs
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    # Rating URLs
    path('products/<int:product_id>/ratings/', views.RatingCreateView.as_view(), name='rating-create'),
    
    # Order URLs
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/status/', views.OrderStatusUpdateView.as_view(), name='order-status-update'),
] 