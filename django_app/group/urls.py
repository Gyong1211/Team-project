from django.conf.urls import url

from group import apis

urlpatterns = [
    url(r'^(?P<pk>\d+)', apis.GroupListCreateView.as_view()),
]
