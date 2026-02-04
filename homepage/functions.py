import dateparser
import requests
from requests.exceptions import JSONDecodeError

from .models import Feedback

LIMIT = 25
BASE_URL = 'https://www.avito.ru'
EXTENSION_URL = '/web/7/user/1f4e0a97fa4bed6be51bb658515d728c/ratings'
PARAMETER_URL = (
    '?limit={limit}&offset={offset}&photoOnly=false&sortRating=date_desc'
)


def create_feedbacks(modeladmin, request, queryset):
    offset = 0
    next_page = True
    count_new = 0
    count = 0

    while next_page:
        try:
            response = requests.get(
                BASE_URL + EXTENSION_URL + PARAMETER_URL.format(
                    limit=LIMIT, offset=offset
                )
            ).json()
        except JSONDecodeError:
            response = 'Ошибка выдачи, неверный запрос'

        next_page = False if response.get('nextPage') is None else True
        offset += LIMIT if next_page else 0

        entries = response.get('entries')

        for item in entries:
            if item.get('type') != 'rating':
                continue

            value = item.get('value')
            if value is None:
                continue

            name_user = value.get('title')
            feedback = (
                value.get('textSections')[0].get('text')
                if value.get('textSections') is not None
                else None
            )
            score = (
                int(value.get('score'))
                if value.get('score') is not None
                else None
            )
            date_create = dateparser.parse(
                value.get('rated'), languages=['ru']
            ).date()
            item_object = value.get('itemTitle')
            item_object = (
                value.get('itemTitle')
                if value.get('itemTitle') is not None
                else None
            )

            answer = value.get('answer')
            answer = answer.get('text') if answer is not None else ''

            new_feedback, create = Feedback.objects.get_or_create(
                name_user=name_user,
                feedback=feedback,
                answer=answer,
                score=score,
                item_object=item_object,
                date_create=date_create
            )
            count += 1
            if create:
                count_new += 1

    return count, count_new
