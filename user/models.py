from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
