from django.contrib import admin
from .models import Product,Category,Variations,Cart,CartItem

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Variations)
admin.site.register(Cart)
admin.site.register(CartItem)

