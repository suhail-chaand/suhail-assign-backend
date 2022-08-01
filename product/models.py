from django.db import models


class Product(models.Model):
    CATEGORIES = (
        ('LAP', 'Laptop'),
        ('DPC', 'Desktop PC'),
        ('NET', 'Networking Device'),
        ('P&S', 'Printer and Scanner'),
        ('PCP', 'PC Port'),
        ('OTH', 'Other')
    )

    category = models.CharField(max_length=3, choices=CATEGORIES, default='OTH')
    model = models.CharField(max_length=20, null=False, blank=False, unique=True)
    brand = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    tagline = models.CharField(max_length=100, null=False, blank=True)
    description = models.TextField(null=False, blank=True)
    price = models.FloatField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    product_id = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image_url
