from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^main/$', apis.PostListCreateView.as_view()),
    url(r'^$', apis.PostListView.as_view()),
    url(r'^my/$', apis.MyPostListCreateView.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.PostRetrieveUpdateDestroyView.as_view()),
]
