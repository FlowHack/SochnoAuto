from django.core.management.base import BaseCommand

from homepage.services.avito_parser import AvitoFeedbackParser


class Command(BaseCommand):
    help = 'Парсинг отзывов со страницы авто'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Запущен парсинг отзывов...'))

        self.stdout.write(self.style.WARNING('Создаю класс парсера'))
        parser = AvitoFeedbackParser()
        self.stdout.write(self.style.WARNING('Парсинг и внесение в БД'))
        total, new = parser.parse_and_save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно завершено! Обработано: {total}, '
                f'Добавлено новых: {new}'
            )
        )
