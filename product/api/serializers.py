from rest_framework import serializers

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_weight(self, value):
        if value <= 0 or value > 25:
            raise serializers.ValidationError("Weight should be a positive decimal and cannot be more than 25 kg.")

        return value
