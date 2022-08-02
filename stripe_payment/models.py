from django.db import models
from product.models import Product


# Create your models here.

class Order(models.Model):
    product_id = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    unit_price = models.FloatField(null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    payment_status = models.CharField(max_length=20, null=False, blank=False)
    customer_email = models.EmailField(max_length=200, null=False, blank=False)
    customer_name = models.CharField(max_length=100, null=False, blank=False)
    customer_address = models.TextField(null=False, blank=False)
    customer_zipcode = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
