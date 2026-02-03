from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import HomepageImage


@admin.register(HomepageImage)
class HomepageImageModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('image', 'order_image', 'caption',)
    empty_value_display = '-пусто-'
