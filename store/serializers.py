from rest_framework import serializers
from .models import Product,Category,Variations,Cart,CartItem

class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variations
        fields = ('id', 'variation_category', 'variation_value', 'is_active', 'created_date')

class ProductSerializer(serializers.ModelSerializer):
    variations = VariationSerializer(many=True, required=False, source='variations_set')

    class Meta:
        model = Product
        fields = ('id', 'product_name', 'slug', 'description', 'price', 'images', 'stock', 'is_available', 'category', 'created_date', 'modified_date', 'variations')       

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'        

    