import datetime

from django import forms


class YearInput(forms.NumberInput):
    def get_context(self, name, value, attrs):
        if isinstance(value, datetime.date):
            value = str(value.year)
        return super().get_context(name, value, attrs)


class CarModelAdminForm(forms.ModelForm):
    year_release = forms.CharField(
        max_length=4,
        widget=YearInput(attrs={'placeholder': 'ГГГГ'})
    )

    def clean(self):
        cleaned_data = super().clean()

        year = cleaned_data.get('year_release')

        if year:
            try:
                if len(year) < 4 or len(year) > 4:
                    raise forms.ValidationError(
                        'Год должен быть числом из 4-ех цифр'
                    )

                year = int(year)

                current_year = datetime.date.today().year

                if year < (current_year - 100) or year > current_year + 1:
                    raise forms.ValidationError(
                        f'Год должен быть между {current_year - 100}'
                        f' и {current_year + 1}'
                    )

                cleaned_data['year_release'] = datetime.date(year, 1, 1)
            except ValueError:
                raise forms.ValidationError('Год должен быть числом')

        return cleaned_data
