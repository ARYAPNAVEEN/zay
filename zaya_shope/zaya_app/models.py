from django.db import models
from django.contrib.auth.models import AbstractUser
from admin_app.models import Products,Category


# Create your models here.
class User(AbstractUser):
   
    email = models.EmailField(unique=True)
    phone = models.CharField( max_length=50, unique=True, null=False, blank=False)
    address = models.TextField(null=True, blank=True)
    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = ["username"] 
    def __str__(self):
        return self.username




class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def total_price(self):
        return self.product.price * self.quantity