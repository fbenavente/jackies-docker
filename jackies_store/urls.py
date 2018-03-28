from django.conf.urls import url
from jackies_store import views


urlpatterns = [
                url(r'^testing/$',
                   views.testing),
                ]
