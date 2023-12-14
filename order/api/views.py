from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from order.api.serializers import OrderSerializer
from order.models import Order


class OrderCreateListAPIView(ListAPIView, CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        # Add the user to the serializer context
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=request.user)
        return Response(serializer.data)

    def get_queryset(self):

        products = self.request.query_params.get('products')
        customer = self.request.query_params.get('customer')

        if products:
            product_list = products.split(',')
            queryset = self.queryset.filter(orderitem__product__name__in=product_list)

        if customer:
            queryset = self.queryset.filter(customer__username=customer)
        else:
            queryset = self.queryset.filter(customer=self.request.user)
        return queryset


class OrderUpdateAPIView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def put(self, request, *args, **kwargs):
        order_id = kwargs.get('pk')
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
