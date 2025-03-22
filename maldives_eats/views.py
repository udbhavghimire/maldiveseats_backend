from django.shortcuts import get_object_or_404
from .models import Category, Product, Order
from rest_framework import generics, status, filters
from rest_framework.response import Response
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    ProductDetailSerializer,
    RatingSerializer, 
    OrderSerializer,
    OrderCreateSerializer
)

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'category__name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get('category', None)
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        return queryset

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'

class RatingCreateView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    
    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        serializer.save(product=product)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        session_id = self.request.query_params.get('session_id', None)
        email = self.request.query_params.get('email', None)
        
        queryset = Order.objects.all()
        
        if session_id:
            queryset = queryset.filter(session_id=session_id)
        
        if email:
            queryset = queryset.filter(email=email)
            
        return queryset

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer

class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['patch']
    
    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        status_value = request.data.get('status')
        
        if status_value and status_value in dict(Order.STATUS_CHOICES).keys():
            order.status = status_value
            order.save()
            return Response({'status': order.status})
        
        return Response(
            {'error': 'Invalid status value'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
