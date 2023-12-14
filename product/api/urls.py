from django.urls import path

from product.api.views import ProductAPIView

urlpatterns = [
    path('products/', ProductAPIView.as_view(), name='products_create_list'),

]
