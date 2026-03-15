import admin_thumbnails
from adminsortable2.admin import (SortableAdminBase, SortableAdminMixin,
                                  SortableStackedInline)
from django.contrib import admin
from dragndrop_related.views import DragAndDropRelatedImageMixin

from .models import Car, CarCategory, CarImage, CarParameter


@admin_thumbnails.thumbnail('image')
class CarImageInline(SortableStackedInline):
    """Настройка добавления изображений при создании/редактировании
    автомобиля"""

    extra = 0
    model = CarImage
    fields = ['image', 'caption', 'order_image']


class CarParameterInline(admin.StackedInline):
    """Настройка добавления параметров автомобиля при создании/редактировании
    автомобиля"""

    model = CarParameter
    extra = 2


@admin.register(Car)
class CarModelAdmin(
    DragAndDropRelatedImageMixin, SortableAdminBase, admin.ModelAdmin
):
    """Модель Автомобиля для административной панели"""

    related_manager_field_name = 'car_images'
    related_model_field_name = 'image'
    related_model_order_field_name = 'order_image'
    inlines = [CarImageInline, CarParameterInline]
    fields = (
        'sold', 'brand', 'model', 'year_release', 'mileage', 'price', 'color',
        'wheel_position', 'fuel_type', 'power_hp', 'engine_capacity',
        'type_transmission', 'car_body', 'category', 'description', 'autoteka'
    )
    list_display = (
        'brand', 'model', 'year_release', 'mileage', 'car_body',
        'fuel_type', 'category', 'sold', 'is_special_offer',
    )
    exclude = (
        'slug', 'pub_date', 'is_special_offer', 'date_is_special_offer',
    )
    empty_value_display = '-пусто-'

    def add_special_offer(self, request, queryset):
        updated = queryset.update(
            is_special_offer=True
        )
        self.message_user(
            request, f'{updated} автомобилей стали специальными предложениями'
        )
    add_special_offer.short_description = 'Сделать специальным предложением'

    def remove_special_offer(self, request, queryset):
        updated = queryset.update(
            is_special_offer=False
        )
        self.message_user(
            request,
            f'{updated} автомобилей удалены из специальных предложений'
        )
    remove_special_offer.short_description = (
        'Убрать из специальных предложений'
    )

    def car_sold(self, request, queryset):
        updated = queryset.update(
            sold=True
        )
        self.message_user(
            request,
            f'{updated} автомобилей указаны как проданные'
        )
    car_sold.short_description = (
        'Проданы'
    )

    actions = [add_special_offer, remove_special_offer, car_sold]


@admin.register(CarCategory)
class CarCategoryModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Модель категорий автомобилей для административной панели"""

    list_display = ('name', 'order_category', 'slug',)
    exclude = ('slug', 'order_category')
    empty_value_display = '-пусто-'
