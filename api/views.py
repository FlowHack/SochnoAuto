from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.views import APIView

from homepage.services import IndexService


class SpecialOffersAPIView(APIView, IndexService):
    """Класс для обработки запросов по специальным предложениям"""

    def get(self, request):
        page = self.get_page_special_offers(request)

        html_special_offers = render_to_string(
            'homepage/partials/cards_special_offers.html',
            {'page_special_offers': page},
            request=request
        )
        html_pagination = render_to_string(
            'homepage/partials/pagination_special_offers.html',
            {'page_special_offers': page},
            request=request
        )

        return Response(
            {
                'html_special_offers': html_special_offers,
                'html_pagination': html_pagination
            }
        )


class FeedbacksAPIView(APIView, IndexService):
    """Класс для обработки запросов по отзывам"""

    def get(self, request):
        page = self.get_page_feedbacks(request)

        html_feedbacks = render_to_string(
            'homepage/partials/cards_feedbacks.html',
            {'page_feedbacks': page},
            request=request
        )
        html_pagination = render_to_string(
            'homepage/partials/pagination_feedbacks.html',
            {'page_feedbacks': page},
            request=request
        )

        return Response(
            {
                'html_feedbacks': html_feedbacks,
                'html_pagination': html_pagination
            }
        )
