from django.conf.urls import url, include
from config.urls import urls_apis, urls_views

urlpatterns = [
    url(r'^api/', include(urls_apis)),
    url(r'', include(urls_views)),
]
