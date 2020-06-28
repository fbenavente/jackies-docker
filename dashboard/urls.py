from django.conf.urls import url
from dashboard.views import (
    dashboard,
    sales,
    sales_by_year,
    sales_by_type,
    sales_by_sku
)

urlpatterns = [
    url(r'^$', dashboard, name='dashboard'),
    url(r'^sales/$', sales, name='sales'),
    url(r'^sales_by_year/$', sales_by_year, name='sales_by_year'),
    url(r'^sales_by_type/$', sales_by_type, name='sales_by_type'),
    url(r'^sales_by_sku/$', sales_by_sku, name='sales_by_sku'),
]
