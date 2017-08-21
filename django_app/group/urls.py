from django.conf.urls import url

from group import apis

app_name = 'group'
urlpatterns = [
    url(r'^$', apis.GroupListCreateView.as_view(), name='group_list'),
    url(r'^my-group/$', apis.MyGroupListView.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.GroupRetrieveUpdateDestroyView.as_view(),),
    url(r'^(?P<pk>\d+)/change-owner/$', apis.GroupOwnerUpdateView.as_view()),
    url(r'^(?P<pk>\d+)/profile-img/', apis.GroupProfileImgDestroyView.as_view()),
    url(r'^tag/$', apis.TagListView.as_view()),
]
