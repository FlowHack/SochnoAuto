from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path

from .models import Feedback, HomepageImage
from .services import AvitoFeedbackParser


@admin.register(HomepageImage)
class HomepageImageModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('image', 'order_image', 'caption',)
    empty_value_display = '-пусто-'


@admin.register(Feedback)
class FeedbackModelAdmin(admin.ModelAdmin):
    change_list_template = 'admin/homepage/feedback/change_list.html'

    list_display = ('name_user', 'score', 'item_object', 'date_create')
    empty_value_display = '-пусто-'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                'parse_avito/',
                self.admin_site.admin_view(self.run_parser_view),
                name='parse_avito'
            ),
        ]
        return my_urls + urls

    def run_parser_view(self, request):
        """Функция, которая вызывается при нажатии на кнопку"""
        try:
            parser = AvitoFeedbackParser()
            total, new = parser.parse_and_save()

            self.message_user(
                request,
                (
                    f'Успешно обработано {total} отзывов. '
                    f'Новых добавлено: {new}'
                ),
                messages.SUCCESS
            )
        except Exception as e:
            self.message_user(
                request,
                f'Ошибка при парсинге: {str(e)}',
                messages.ERROR
            )
            raise Exception(e)

        return HttpResponseRedirect("../")
