from django.conf.urls import url

from . import apis

app_name = 'member'
urlpatterns = [
    url(r'^$', apis.UserListCreateView.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.UserRetrieveUpdateDestroyView.as_view()),
    url(r'^(?P<pk>\d+)/profile_img/', apis.UserProfileImgDestroyView.as_view()),
    url(r'^(?P<pk>\d+)/password_update/$', apis.UserPasswordUpdateView.as_view()),
    url(r'^(?P<pk>\d+)/follower/$', apis.UserFollowerListView.as_view()),
    url(r'^(?P<pk>\d+)/following/$', apis.UserFollowingListView.as_view()),
    url(r'^login/', apis.LoginView.as_view()),
    url(r'^logout/', apis.LogoutView.as_view()),
    url(r'^relation/$', apis.UserRelationCreateDestroyView.as_view()),
    url(r'^membership/$', apis.MembershipCreateDestroyView.as_view()),
]
