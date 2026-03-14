from django.contrib import admin
from .models import Order, OrderItem

class ItemInline(admin.TabularInline):
    model=OrderItem; extra=0; readonly_fields=['product_name','price','qty','weight_kg']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['order_id','full_name','mobile','total','status','created_at']
    list_filter=['status','courier','state']; search_fields=['order_id','full_name','mobile']
    list_editable=['status']; readonly_fields=['order_id','created_at']; inlines=[ItemInline]
