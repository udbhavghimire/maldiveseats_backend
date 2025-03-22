from rest_framework import serializers
from .models import Category, Product, Rating, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug','icon']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rating', 'comment', 'created']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    average_rating = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'category_name', 'title', 'slug', 'image', 
                  'description', 'price', 'unit', 'stock', 'available', 
                  'created', 'updated', 'average_rating']

class ProductDetailSerializer(ProductSerializer):
    ratings = RatingSerializer(many=True, read_only=True)
    
    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['ratings']

class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.ReadOnlyField(source='product.title')
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'price', 'quantity', 'get_total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'name', 'email', 'phone', 'address', 'session_id', 
                  'total_price', 'status', 'created', 'updated', 'items']
        read_only_fields = ['created', 'updated']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = serializers.ListField(
        child=serializers.DictField(), 
        write_only=True
    )
    
    class Meta:
        model = Order
        fields = ['name', 'email', 'phone', 'address', 'session_id', 'total_price', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            product_id = item_data.get('product_id')
            quantity = item_data.get('quantity', 1)
            
            try:
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=quantity
                )
            except Product.DoesNotExist:
                pass
        
        return order 