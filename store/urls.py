from django.urls import path,include

from store import views

urlpatterns = [
    path('categories/',views.CategoryListAPIView.as_view(), name='category-list'),
    path('products/',views.ProductList.as_view()),
    path('product_detail/<slug:category_slug>/<slug:product_slug>/',views.ProductDetail.as_view()),
    path('addcart/<int:item_id>/<str:value>/',views.AddtoCart.as_view()),
    path('Search_item/',views.Search.as_view(),name='Search_item'),
]
