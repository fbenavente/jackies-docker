from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from management.serializers import *
from management.models import *
import arrow
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator


def testing(request):
    return render(request, 'jackies_store/testing.html')


class IndexView(TemplateView):
    template_name = 'landing/index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


def new_order(request):
    # flavors
    flavors = []
    for flavor in Flavor.objects.filter(category_id=10).order_by('name'):
        flavors.append({'name': flavor.name, 'id': flavor.id})

    valid_size_ids = [16, 6, 8, 13]

    price_data = {}
    for flavor in flavors:
        for size in valid_size_ids:
            if not price_data.get(flavor['id']):
                price_data[flavor['id']] = {}
            if not price_data[flavor['id']].get(size):
                price_data[flavor['id']][size] = None

            try:
                product = Product.objects.get(category_id=10, flavor_id=flavor['id'], size_id=size)
                price_data[flavor['id']][size] = {'price': product.price, 'id': product.id}
            except:
                price_data[flavor['id']][size] = {'price': 'NON-EXISTING', 'id': ''}
    return render(request, 'landing/final_cart.html', context={
        'flavors': flavors,
        'price_data': price_data,
        'default_flavor': None,
        'default_size': None,
        'retire_times': get_retire_time_days()
    })


def get_day_format(from_day):
    locale = arrow.locales.get_locale('es')
    day_name = locale.day_name(from_day.isoweekday())
    month_name = locale.month_name(from_day.month)
    return u'{} {} de {}'.format(day_name, from_day.day, month_name)


def get_retire_time_days():
    days = []
    now = arrow.now()
    from_day = now.replace(days=2)
    if from_day.weekday() == 6:  # Sunday
        from_day.replace(days=1)
    days.append({'text': get_day_format(from_day), 'val': from_day.format('DD/MM/YYYY')})
    while len(days) < 7:
        day = from_day.replace(days=1)
        if day.weekday() == 6:  # Sunday
            day.replace(days=1)
        days.append({'text': get_day_format(day), 'val': day.format('DD/MM/YYYY')})
    return days



"""
def get_retire_time_days():
    locale = arrow.locales.get_locale('es')
    now = arrow.now()
    from_day = now.replace(days=2)
    day_name = locale.day_name(from_day.isoweekday())
    month_name = locale.month_name(from_day.month)
    date = u'{} {} de {}'.format(day_name, from_day.day, month_name)
    return date
"""