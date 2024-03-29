"""jackies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from jackies_store.views import IndexView
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^pos/', include('pos.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^management/', include('management.urls')),
    url(r'^jackies_store/', include('jackies_store.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url('^.*$', IndexView.as_view(), name='index'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    #url('^.*$', IndexView.as_view(), name='index'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
