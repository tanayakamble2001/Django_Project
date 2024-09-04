from django.contrib import admin
from .models import Category,Product,Cart
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','category_name']
admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','p_name','p_price','p_description','category']
    list_filter=['p_name','p_price','category']
admin.site.register(Product,ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']
admin.site.register(Cart,CartAdmin)