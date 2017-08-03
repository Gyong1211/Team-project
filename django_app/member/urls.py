from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^$', apis.UserListCreateView.as_view()),
    url(r'^(?P<pk>\d+)/', apis.UserUpdateView.as_view()),
    # url(r'^login/', apis.AuthTokenView)
]
