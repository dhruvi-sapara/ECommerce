from django.utils import timezone
from rest_framework import serializers

from order.models import OrderItem, Order
from product.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True)
    customer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'order_number', 'customer', 'order_date', 'address', 'orderitem_set')
        read_only_fields = ('id', 'order_number',)

    def validate(self, data):
        # Validation for order date
        order_date = data.get('order_date')
        if order_date < timezone.now().date():
            raise serializers.ValidationError("Order date cannot be in the past.")

        # Validation for cumulative weight
        total_weight = sum(item.weight for item in data['orderitem_set'])
        if total_weight > 150:
            raise serializers.ValidationError("Cumulative weight must be under 150kg.")

        return data

    def create(self, validated_data):
        order_items_data = validated_data.pop('orderitem_set')

        order = Order.objects.create(**validated_data)

        # Associate each order item with the created order
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('orderitem_set', [])

        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        for order_item_data in order_items_data:
            product_data = order_item_data.get('product_set')
            product_id = product_data.get('id') if product_data else None

            if product_id:
                product = Product.objects.get(id=product_id)
                quantity = order_item_data.get('quantity')

                order_item, created = OrderItem.objects.get_or_create(order=instance, product=product)
                order_item.quantity = quantity
                order_item.save()

        return instance
