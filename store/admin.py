from django.contrib import admin
from .models import Category, Product, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug','emoji','sort_order']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category','price','offer_price','stock','is_featured','is_active']
    list_filter  = ['category','is_featured','is_new_arrival','is_active']
    list_editable= ['is_featured','is_active']
    search_fields= ['name']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name','location','rating','verified','created_at']
