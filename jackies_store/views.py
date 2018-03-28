from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from management.serializers import *
from management.models import *
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator

def testing(request):
    return render(request, 'jackies_store/testing.html')


class IndexView(TemplateView):
    template_name = 'jackies_store/index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)
