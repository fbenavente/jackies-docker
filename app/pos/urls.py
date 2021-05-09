from django.conf.urls import url
from pos.views import (
    sale,
    checkout,
    orders,
    order,
    confirm_order,
    new_order,
    checkout_new_order,
    change_order_status,
    real_cart,
    web_order,
    autologin,
    web_checkout,
    post_checkout,
    login,
    edit_order
)

urlpatterns = [
    url(r'^$', orders, name='pos_index'),
    url(r'^sale/$', sale, name='pos_sale'),
    url(r'^checkout/$', checkout, name='pos_checkout'),
    url(r'^orders/$', orders, name='pos_orders'),
    url(r'^jackies452314181424/$', autologin, name='autologin'),
    url(r'^edit_order/$', edit_order, name='edit_order'),
    url(r'^login/$', login, name='login'),
    url(r'^order/(?P<order_id>[\d]+)$', order, name='pos_order'),
    url(r'^confirm_order/$', confirm_order, name='pos_confirm_order'),
    url(r'^new_order/$', new_order, name='pos_new_order'),
    url(r'^checkout_new_order/$', checkout_new_order, name='pos_checkout_new_order'),
    url(r'^change_order_status/$', change_order_status, name='change_order_status'),
    url(r'^real_cart/$', real_cart, name='real_cart'),
    url(r'^web_order/$', web_order, name='web_order'),
    url(r'^web_checkout/$', web_checkout, name='web_checkout'),
    url(r'^post_checkout/$', post_checkout, name='post_checkout'),
]