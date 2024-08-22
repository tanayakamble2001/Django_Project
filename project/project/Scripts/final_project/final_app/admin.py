from django.contrib import admin
from .models import Category,Product
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','category_name']
admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','p_name','p_price','p_description','category']
    list_filter=['p_name','p_price']
admin.site.register(Product,ProductAdmin)