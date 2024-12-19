from django.contrib import admin

# Register your models here.
from .models import Product, AuditTrail


# admin -->register
# register the pdt model with admin interface
@admin.register(Product)
# class produt admin-->cutomized pdt model with admin inetrface
class ProductAdmin(admin.ModelAdmin):
    # pdt display field
    list_display=('name','description','stock_quantity','price', 'user', 'date_created', 'date_modified')
    # to add filter--allowing user -->create and modify date
    list_filter=('user','date_created','date_modified')
    # search functionality
    search_fields=('name','description')

    
# audit trail-->registration with admin interface
@admin.register(AuditTrail)
# class audit trail admin
class AuditTrailAdmin(admin.ModelAdmin):
    # to display
    list_display=('product','version','name','stock_quantity', 'price', 'user', 'timestamp')
    # to filter
    list_filter=('product','user','timestamp')
    # to search
    search_fields=('product__name','name')