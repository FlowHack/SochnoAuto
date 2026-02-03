from django.contrib import admin
from adminsortable2.admin import SortableStackedInline
from .forms import CarModelAdminForm
from .models import (Car, CarCategory, CarComfortParameter, CarImage,
                     CarParameter)
from adminsortable2.admin import SortableAdminBase


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
    list_display = (
        'brand', 'car_model', 'year_release', 'mileage',
        'fuel_type', 'category', 'is_special_offer',
    )
    exclude = ('slug', 'pub_date',)
    empty_value_display = '-пусто-'


@admin.register(CarCategory)
class CarCategoryModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'image',)
    exclude = ('slug',)
    empty_value_display = '-пусто-'
