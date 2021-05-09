from django.conf.urls import url, include
from management import views
from rest_framework import routers
from management.views import CustomUserViewSet
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from management.views import LoginView, LogoutView


router = routers.SimpleRouter()
router.register(r'customuser', CustomUserViewSet)

urlpatterns = [
                url(r'^manage_backgrounds/$',
                   views.BackgroundList.as_view(),
                   name='admin_backgrounds'),
                url(r'^manage_categories/$',
                   views.CategoryList.as_view(),
                   name='admin_categories'),
                url(r'^manage_categories/(?P<pk>[\d]+)$',
                   views.CategoryDetail.as_view(),
                   name='admin_categories_with_pk'),
                url(r'^manage_orders/$',
                   views.OrderList.as_view(),
                   name='admin_orders'),
                url(r'^manage_orders/(?P<pk>[\d]+)$',
                   views.OrderDetail.as_view(),
                   name='admin_orders_with_pk'),
                url(r'^manage_products/$',
                   views.ProductList.as_view(),
                   name='admin_products'),
                url(r'^manage_products2/$',
                   views.ProductList2.as_view(),
                   name='admin_products'),
                url(r'^manage_products/(?P<pk>[\d]+)$',
                   views.ProductDetail.as_view(),
                   name='admin_products_with_pk'),
                url(r'^manage_users/',include(router.urls)),
                url(r'^register/$', TemplateView.as_view(template_name="management/register.html"), name='user_register'),
                url(r'^auth/login/$', LoginView.as_view(), name='login'),
                url(r'^auth/logout/$', LogoutView.as_view(), name='logout'),
                ]
