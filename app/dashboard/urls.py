from django.conf.urls import url
from dashboard.views import (
    dashboard,
    sales,
    incomes_vs_costs,
    sales_by_year,
    sales_by_type,
    sales_by_sku
)

urlpatterns = [
    url(r'^$', dashboard, name='dashboard'),
    url(r'^sales/$', sales, name='sales'),
    url(r'^incomes_costs/$', incomes_vs_costs, name='incomes_vs_costs'),
    url(r'^sales_by_year/$', sales_by_year, name='sales_by_year'),
    url(r'^sales_by_type/$', sales_by_type, name='sales_by_type'),
    url(r'^sales_by_sku/$', sales_by_sku, name='sales_by_sku'),
]
