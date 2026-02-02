from django.contrib import admin

from .models import HomepageImage


@admin.register(HomepageImage)
class HomepageImage(admin.ModelAdmin):
    list_display = ('image', 'caption',)
    empty_value_display = '-пусто-'
