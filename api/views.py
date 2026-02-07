from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Prefetch
from rest_framework.decorators import api_view
from rest_framework.response import Response

from auto_store.models import Car, CarCategory, CarImage
from auto_store.settings import NUMBER_ITEM_PAGINATOR_CARS
from homepage.models import Feedback
from homepage.settings import (NUMBER_ITEM_PAGINATOR_FEEDBACKS,
                               NUMBER_ITEM_PAGINATOR_SPECIAL_OFFERS)

from .serializer import CarWithImagesSerializer


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


@api_view(['GET'])
def get_special_offers(request):
    page = request.GET.get('special_offers_page')

    special_offers_qs = Car.objects.filter(
        is_special_offer=True, sold=False
    ).order_by('date_is_special_offer').prefetch_related(
        Prefetch(
            'car_images',
            CarImage.objects.order_by('order_image'),
            to_attr='ordered_images'
        )
    )
    serializer = CarWithImagesSerializer(special_offers_qs, many=True)
    paginator = Paginator(
        serializer.data, NUMBER_ITEM_PAGINATOR_SPECIAL_OFFERS
    )
    try:
        page_special_offers = paginator.get_page(
            page
        )
    except PageNotAnInteger:
        page_special_offers = paginator.page(1)
    except EmptyPage:
        page_special_offers = paginator.page(
            paginator.num_pages
        )

    has_next = page_special_offers.has_next()
    has_previous = page_special_offers.has_previous()

    return Response(
        {
            'objects': list(page_special_offers.object_list),
            'has_next': has_next,
            'has_previous': has_previous
        }
    )


@api_view(['GET'])
def get_cars_in_category(request):
    selected_category = request.GET.get('category')
    page = request.GET.get('page')

    category = CarCategory.objects.filter(
        slug=selected_category
    ).first()

    objects = None
    has_next = None
    has_previous = None
    if category:
        cars = category.cars_in_category.all().prefetch_related(
            Prefetch(
                'car_images',
                CarImage.objects.order_by('order_image'),
                to_attr='ordered_images'
            )
        )
        serializer = CarWithImagesSerializer(cars, many=True)
        paginator = Paginator(serializer.data, NUMBER_ITEM_PAGINATOR_CARS)
        try:
            page_cars = paginator.get_page(
                page
            )
        except PageNotAnInteger:
            page_cars = paginator.page(1)
        except EmptyPage:
            page_cars = paginator.page(
                paginator.num_pages
            )
        objects = list(page_cars.object_list)

        has_next = page_cars.has_next()
        has_previous = page_cars.has_previous()

    return Response(
        {
            'objects': objects,
            'has_next': has_next,
            'has_previous': has_previous
        }
    )
