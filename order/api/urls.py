from django.urls import path

from order.api.views import OrderCreateListAPIView, OrderUpdateAPIView

urlpatterns = [
    path('orders/', OrderCreateListAPIView.as_view(), name='create_list_orders'),
    path('orders/<int:pk>/', OrderUpdateAPIView.as_view(), name='update_orders'),

]
