from django.conf.urls import url
from dashboard.views import dashboard, sales

urlpatterns = [
    url(r'^$', dashboard, name='dashboard'),
    url(r'^sales/$', sales, name='sales'),
]
