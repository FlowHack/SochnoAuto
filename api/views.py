from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response

from homepage.models import Feedback
from homepage.settings import NUMBER_ITEM_PAGINATOR_FEEDBACKS


@api_view(['GET'])
def get_feedbacks(request):
    page = request.GET.get('page_feedbacks')
    feedbacks = Feedback.objects.all().values(
        'name_user', 'feedback', 'answer', 'score', 'item_object',
        'date_create'
    )

    paginator = Paginator(feedbacks, NUMBER_ITEM_PAGINATOR_FEEDBACKS)
    try:
        page_feedbacks = paginator.get_page(page)
    except PageNotAnInteger:
        page_feedbacks = paginator.page(1)
    except EmptyPage:
        page_feedbacks = paginator.page(paginator.num_pages)

    has_next = page_feedbacks.has_next()
    has_previous = page_feedbacks.has_previous()

    return Response(
        {
            'objects': list(page_feedbacks.object_list),
            'has_next': has_next,
            'has_previous': has_previous
        }
    )
