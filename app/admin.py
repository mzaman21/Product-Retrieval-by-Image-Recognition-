from django.contrib import admin

# Register your models here.
from .models import Brand, Product, PImage,Customer,OrderItem,Order

admin.site.register(Brand)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(Order)

# admin.site.register(Product)
# admin.site.register(PImage)

class ProductImageAdmin(admin.StackedInline):
    model = PImage
@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    class Meta:
        model = Product
@admin.register(PImage)

class ProductImageAdmin(admin.ModelAdmin):
    pass