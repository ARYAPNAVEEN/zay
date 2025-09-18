from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category_images/',blank=True,null=True)
    def __str__(self):
        return self.name

class Products(models.Model):
    
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    discount_price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models. CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True) 
    stock = models.PositiveIntegerField(default=0)
    # discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
       return self.name
    



class Discount(models.Model):
    name = models.CharField(max_length=100)   
    percentage = models.PositiveIntegerField(default=0)  
    active = models.BooleanField(default=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    def __str__(self):
        return self.name




