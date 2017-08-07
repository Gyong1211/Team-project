from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^mygroup/$', apis.MyGroupPostListView.as_view()),
    url(r'^$', apis.PostListCreateView.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.PostRetrieveUpdateDestroyView.as_view()),
    url(r'^(?P<pk>\d+)/comment/$', apis.CommentCreateView.as_view()),
    url(r'^comment/(?P<pk>\d+)/$', apis.CommentRetrieveUpdateDestroyView.as_view()),
]
