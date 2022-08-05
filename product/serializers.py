from rest_framework import serializers
from .models import (Image,
                     Product)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'product_id', 'image_url']
        extra_kwargs = {'product_id': {'read_only': True}}


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'model', 'brand', 'name', 'tagline', 'description', 'price', 'images']

    def create(self, validated_data):
        images = validated_data.pop('images')
        product = Product.objects.create(**validated_data)
        for image in images:
            Image.objects.create(product_id=product, **image)
        return product
