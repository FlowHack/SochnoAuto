import logging
import os
from datetime import date
from io import BytesIO
from urllib.parse import urlparse

import dateparser
import requests
from django.conf import settings
from django.core.files import File
from requests.exceptions import RequestException

from homepage.models import Feedback

logger = logging.getLogger(__name__)


class AvitoFeedbackParser:
    """Класс парсера отзывов с авито"""

    BASE_URL = 'https://www.avito.ru'
    API_ENDPOINT = f'/web/7/user/{settings.AVITO_USER_ID}/ratings'
    HEADERS = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/142.0.0.0 YaBrowser/25.12.0.0 Safari'
            '/537.36'
        ),
        'Accept': 'application/json, text/plain, */*'
    }

    def __init__(self, limit: int = 25):
        self.limit = limit
        self.count_total = 0
        self.count_new = 0

    def parse_and_save(self) -> tuple[int, int]:
        """Главный метод запуска парсинга

        Return: Всего отзывов обработано, отзывов из них добавлено
        """

        offset = 0
        has_next = True

        while has_next:
            url_parameters = (
                f'?limit={self.limit}&offset={offset}&photoOnly=false&'
                'sortRating=date_desc'
            )
            url_request = f'{self.BASE_URL}{self.API_ENDPOINT}{url_parameters}'

            try:
                response = requests.get(url_request, headers=self.HEADERS)
                response.raise_for_status()
                data = response.json()
            except RequestException as e:
                logger.error(f'Ошибка при запросе к Авито: {e}')
                break
            except ValueError as e:
                logger.error(f'Не удалось декодировать полученные данные: {e}')
                break

            entries = data.get('entries', [{}])
            self._processin_feedbacks_from_page(entries)

            next_page = data.get('nextPage')
            if next_page is not None:
                offset += self.limit
            else:
                has_next = False

        return self.count_total, self.count_new

    def _processin_feedbacks_from_page(self, entries: list):
        """Получение данных со страницы выдачи отзывов"""

        for item in entries:
            if item.get('type') != 'rating':
                continue

            value = item.get('value', {})
            if not value:
                continue

            self._create_or_update_feedback(value)

    def _create_or_update_feedback(self, value: dict):
        """Извлечение полученных данных и внесение их в БД"""

        feedback_avito_id = value.get('id')
        if not feedback_avito_id:
            return

        avatar_value = value.get('avatar', None)
        if avatar_value is not None:
            avatar_url = (
                avatar_value.get('36x36') or avatar_value.get('64x64') or
                avatar_value.get('48x48') or avatar_value.get('50x50') or
                avatar_value.get('60x40') or avatar_value.get('96x64')
            )
        avatar = self._download_avatar(avatar_url)

        defaults = {
            'name_user': value.get('title', 'Аноним'),
            'feedback': value.get('textSections', [{}])[0].get('text'),
            'score': value.get('score'),
            'item_object': value.get('itemTitle'),
            'answer': value.get('answer', {}).get('text'),
            'avatar': avatar if avatar else None
        }

        rated = dateparser.parse(
            value.get('rated'), languages=['ru']
        ).date()
        defaults['date_create'] = rated if rated else date.today()

        obj, create = Feedback.objects.update_or_create(
            feedback_avito_id=feedback_avito_id,
            defaults=defaults
        )

        self.count_total += 1
        if create:
            self.count_new += 1

    def _download_avatar(self, avatar_url: str) -> File | None:
        """Метод загружает аватар и возвращает Django File object для
        прикрепления его к модели

        Args:
            avatar_url: Ссылка на автар, который необходимо скачать

        Return: Объект картинки дял прикрепления к модели
        """

        if not avatar_url:
            return None

        try:
            response = requests.get(avatar_url, timeout=10)
            response.raise_for_status()

            image_content = BytesIO(response.content)

            parsed_url = urlparse(avatar_url)
            filename = os.path.basename(parsed_url.path)
            if not filename or '.' not in filename:
                filename = 'avatar.jpg'

            file_obj = File(image_content, name=filename)
            return file_obj
        except RequestException as e:
            logger.warning(
                f'Ошибка при скачивании аватара "{avatar_url}": {e}'
            )

        return None
