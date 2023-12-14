from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from product.api.serializers import ProductSerializer
from product.models import Product


class ProductAPIView(ListAPIView, CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
