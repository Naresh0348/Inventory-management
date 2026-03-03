from django.contrib import admin
from .models import Category, Product, Sales, Supplier, PurchaseOrder

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'email', 'phone')
    search_fields = ('company_name', 'contact_person')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'supplier', 'price', 'stock_level', 'threshold', 'low_stock_alert')
    search_fields = ('sku', 'name')
    list_filter = ('category', 'supplier')
    list_editable = ('price', 'stock_level', 'threshold')

    def low_stock_alert(self, obj):
        return obj.is_low_stock
    low_stock_alert.boolean = True
    low_stock_alert.short_description = 'Low stock?'

@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'product', 'quantity', 'sale_date', 'status')
    search_fields = ('customer_name', 'status')
    list_filter = ('status', 'sale_date')
    readonly_fields = ('sale_date',)

@admin.register(PurchaseOrder)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'supplier', 'quantity', 'order_date', 'status')
    search_fields = ('product', 'supplier')
    list_filter = ('supplier',)
    list_editable = ('status',)