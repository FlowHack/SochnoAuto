from django import forms

from cars.models import Car

from .models import RequestContact
from .services import ContactService


class RequestContactForm(forms.ModelForm):
    type_request = forms.ChoiceField(
        choices=RequestContact.TypeRequest.choices,
        widget=forms.HiddenInput()
    )
    car_slug = forms.SlugField(
        required=False, widget=forms.HiddenInput()
    )

    class Meta:
        model = RequestContact
        fields = ['name', 'email', 'telephone_number']

    def clean(self):
        cleaned_data = super().clean()

        type_request = cleaned_data.get('type_request')
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        car_slug = cleaned_data.get('car_slug')

        if not all([type_request, name, email]):
            return cleaned_data

        car = None
        if car_slug:
            try:
                car = Car.objects.get(slug=car_slug)
            except Car.DoesNotExist:
                raise forms.ValidationError(
                    'Указанный автомобиль не найден. Сообщите нам об ошибке'
                    ' через форму "Связаться с нами"'
                )

        type_request_need_car = [
            RequestContact.TypeRequest.AUTOTEKA,
            RequestContact.TypeRequest.CONTACT_CAR
        ]
        if not car_slug and type_request in type_request_need_car:
            raise forms.ValidationError(
                'Автомобиль не указан. Сообщите нам об ошибке'
                ' через форму "Связаться с нами"'
            )

        has_duplicate = ContactService().check_duplicate_request(
            type_request, name, email, car
        )

        if has_duplicate == 'confirmed':
            raise forms.ValidationError(
                'Ваша заявка уже в работе! Мы обязательно ответим Вам.'
            )

        if has_duplicate == 'unconfirmed':
            raise forms.ValidationError(
                'Вы уже создавали такую заявку. Проверьте почту и '
                'подтвердите email для обработки заявки.'
            )

        cleaned_data['car'] = car

        return cleaned_data
