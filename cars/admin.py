from adminsortable2.admin import (SortableAdminBase, SortableAdminMixin,
                                  SortableStackedInline)
from django.contrib import admin

from .models import Car, CarCategory, CarImage, CarParameter


class CarImageInline(SortableStackedInline):
    """Настройка добавления изображений при создании/редактировании
    автомобиля"""

    model = CarImage
    extra = 2


class CarParameterInline(admin.StackedInline):
    """Настройка добавления параметров автомобиля при создании/редактировании
    автомобиля"""

    model = CarParameter
    extra = 2


@admin.register(Car)
class CarModelAdmin(SortableAdminBase, admin.ModelAdmin):
    """Модель Автомобиля для административной панели"""

    inlines = [CarImageInline, CarParameterInline]
    fields = (
        'sold', 'brand', 'model', 'year_release', 'mileage', 'fuel_type',
        'price', 'power_hp', 'color', 'wheel_position', 'engine_capacity',
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
