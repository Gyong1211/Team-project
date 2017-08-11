from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^mygroup/$', apis.MyGroupPostListView.as_view()),
    url(r'^$', apis.PostListCreateView.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.PostRetrieveUpdateDestroyView.as_view()),
    url(r'^(?P<pk>\d+)/postliketoggle/$', apis.PostLikeToggle.as_view()),
    url(r'^comment/$', apis.CommentListCreateView.as_view()),
    url(r'^comment/(?P<pk>\d+)/$', apis.CommentRetrieveUpdateDestroyView.as_view()),
]
