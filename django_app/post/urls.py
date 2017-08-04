from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^mygroup/$', apis.MyGroupPostListView.as_view()),
    url(r'^$', apis.PostListCreateView.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.PostRetrieveUpdateDestroyView.as_view()),
]
