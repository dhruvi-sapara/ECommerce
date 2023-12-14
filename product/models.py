from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
