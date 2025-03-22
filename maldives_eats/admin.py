from django.contrib import admin
from .models import Category, Product, Rating, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0
    readonly_fields = ['created']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [RatingInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'status', 'total_price', 'created']
    list_filter = ['status', 'created', 'updated']
    search_fields = ['name', 'email', 'phone']
    inlines = [OrderItemInline]
    list_editable = ['status']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['product', 'rating', 'created']
    list_filter = ['rating', 'created']
    search_fields = ['product__title', 'comment']
