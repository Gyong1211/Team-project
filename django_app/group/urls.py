from django.conf.urls import url

from group import apis

urlpatterns = [
    url(r'^$', apis.GroupListCreateView.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.GroupRetrieveView.as_view()),
    url(r'^(?P<pk>\d+)/member/$', apis.GroupMemberListView.as_view()),
]
