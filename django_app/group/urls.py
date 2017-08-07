from django.conf.urls import url

from group import apis

urlpatterns = [
    url(r'^$', apis.GroupListCreateView.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.GroupRetrieveUpdateDestroyView.as_view()),
    url(r'^(?P<pk>\d+)/change_owner/$', apis.GroupOwnerUpdateView.as_view()),
    url(r'^(?P<pk>\d+)/profile_img/', apis.GroupProfileImgDestroyView.as_view()),
    url(r'^tag/$', apis.TagListCreateView.as_view()),
]
