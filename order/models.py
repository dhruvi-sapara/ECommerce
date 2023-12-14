from django.db import models

from product.models import Product
from user.models import User


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_number = models.CharField(max_length=10, unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField()
    address = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Auto-generate order_number if not provided
        if not self.order_number:
            last_order = Order.objects.order_by('-id').first()
            if last_order:
                last_order_number = int(last_order.order_number[3:])
                self.order_number = f'ORD{str(last_order_number + 1).zfill(5)}'
            else:
                self.order_number = 'ORD00001'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order: {self.order.order_number}, Product: {self.product.name}, Quantity: {self.quantity}"
