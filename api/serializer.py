from rest_framework import serializers

from auto_store.models import Car, CarImage


class CarImageSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source='image.url')

    class Meta:
        model = CarImage
        fields = ['image_url', 'caption', 'order_image']


class CarWithImagesSerializer(serializers.ModelSerializer):
    ordered_images = CarImageSerializer(source='car_images', many=True)

    class Meta:
        model = Car
        fields = [
            'brand', 'car_model', 'year_release', 'price', 'slug',
            'ordered_images', 'mileage'
        ]
