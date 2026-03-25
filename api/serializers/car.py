from rest_framework import serializers

from cars.models import Car, CarImage


class CarImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CarImage, который включает URL изображения,
    подпись и порядок отображения.
    """

    image_url = serializers.CharField(source='image.url')

    class Meta:
        model = CarImage
        fields = ['image_url', 'caption', 'order_image']


class CarWithImagesSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Car, который включает информацию об изображениях.
    """

    ordered_images = CarImageSerializer(source='car_images', many=True)

    class Meta:
        model = Car
        fields = [
            'brand', 'model', 'year_release', 'price', 'slug',
            'ordered_images', 'mileage', 'engine_capacity', 'type_transmission'
        ]
