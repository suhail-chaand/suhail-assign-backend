from rest_framework import serializers
from .models import Product, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'product_id', 'image_url']


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'model', 'brand', 'name', 'tagline', 'description', 'price', 'images']
