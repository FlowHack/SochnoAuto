from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import RequestContact


class ExpiredFilter(SimpleListFilter):
    title = _('Истекшие токены')
    parameter_name = 'expired_tokens'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Да')),
            ('no', _('Нет')),
        )

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == 'yes':
            return queryset.filter(
                expires_at__lt=now,
                status=RequestContact.Status.WAIT_EMAIL_CONFIRMATION
            )
        if self.value() == 'no':
            return queryset.filter(
                expires_at__gte=now,
                status=RequestContact.Status.WAIT_EMAIL_CONFIRMATION
            )
        return queryset


@admin.register(RequestContact)
class RequestContactModelAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'type_request', 'status', 'created_at', 'expires_at'
    )
    list_filter = [ExpiredFilter, 'type_request', 'status']
    empty_value_display = '-пусто-'
