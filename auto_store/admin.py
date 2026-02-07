from adminsortable2.admin import (SortableAdminBase, SortableAdminMixin,
                                  SortableStackedInline)
from django.contrib import admin
from django.utils import timezone

from .forms import CarModelAdminForm
from .models import (Car, CarCategory, CarComfortParameter, CarImage,
                     CarParameter)


class CarImageInline(SortableStackedInline):
    model = CarImage
    extra = 2


class CarParameterInline(admin.StackedInline):
    model = CarParameter
    extra = 2


class CarComfortParameterInline(admin.StackedInline):
    model = CarComfortParameter
    extra = 2


@admin.register(Car)
class CarModelAdmin(SortableAdminBase, admin.ModelAdmin):
    form = CarModelAdminForm
    inlines = [CarImageInline, CarParameterInline, CarComfortParameterInline]
    fields = (
        'sold', 'brand', 'car_model', 'year_release', 'mileage', 'fuel_type',
        'price', 'category',
    )
    list_display = (
        'brand', 'car_model', 'year_release', 'mileage',
        'fuel_type', 'category', 'sold', 'is_special_offer', 'slug',
    )
    exclude = ('slug', 'pub_date', 'is_special_offer', 'date_is_special_offer')
    empty_value_display = '-пусто-'

    def add_special_offer(self, request, queryset):
        updated = queryset.update(
            is_special_offer=True,
            date_is_special_offer=timezone.now()
        )
        self.message_user(
            request, f'{updated} автомобилей стали специальными предложениями'
        )
    add_special_offer.short_description = 'Сделать специальным предложением'

    def remove_special_offer(self, request, queryset):
        updated = queryset.update(
            is_special_offer=False,
            date_is_special_offer=None
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
            f'{updated} автомобилей указаны как проданы'
        )
    car_sold.short_description = (
        'Проданы'
    )

    actions = [add_special_offer, remove_special_offer, car_sold]


@admin.register(CarCategory)
class CarCategoryModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'order_category', 'slug',)
    exclude = ('slug', 'order_category')
    empty_value_display = '-пусто-'
