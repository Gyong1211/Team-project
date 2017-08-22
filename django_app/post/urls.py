from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^$', apis.PostListCreateView.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.PostRetrieveUpdateDestroyView.as_view()),
    url(r'^(?P<pk>\d+)/post-like-toggle/$', apis.PostLikeToggleView.as_view()),
    url(r'^my-group/$', apis.MyGroupPostListView.as_view()),
    url(r'^comment/$', apis.CommentListCreateView.as_view()),
    url(r'^comment/(?P<pk>\d+)/$', apis.CommentUpdateDestroyView.as_view()),
]
