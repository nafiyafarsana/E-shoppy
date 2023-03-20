from django.shortcuts import render
from django.http import Http404
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter,OrderingFilter

from .models import Product,Cart,CartItem,Variations,Category
from .serializers import ProductSerializer,CartItemSerializer,CartSerializer,CategorySerializer

# Create your views here.

class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class ProductList(APIView):
    def get(self,request,formt=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)

class ProductDetail(APIView):
    def get_object(self,category_slug,product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
        
    def get(self,request,category_slug,product_slug,format=None):
        product = self.get_object(category_slug,product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
class AddtoCart(APIView):
    def post(self,request,item_id,value):
        try:
            item = CartItem.objects.get(id=item_id)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        
       
        cart = Cart.objects.get_or_create(user=request.user)[0]
        product = Product.objects.get(id=item_id)
        variation = Variations.objects.get(variation_value=value)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, user=request.user)
        cart_item.variations.set([variation])
        if not created:
            if variation in cart_item.variations.all():
                cart_item.quantity += 1
                cart_item.save()
            else:
                cart_item.variations.add(variation)
        else:
            cart_item.quantity = 1
            cart_item.save()
            cart_item.variations.add(variation)
        cart_serializer = CartItemSerializer(cart_item)
        return Response(cart_serializer.data, status=status.HTTP_200_OK)
    
class Search(APIView):
    def get(self,request):
        s = request.GET.get('s')
        item = Product.objects.all()
        if s:
            item = Product.objects.filter(product_name__icontains=s)
        serializer = ProductSerializer(item,many = True)
        return Response(serializer.data)