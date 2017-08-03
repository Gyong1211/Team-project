from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^(?P<pk>\d+)/', apis.UserUpdateView.as_view()),


    url(r'^login/', apis.LoginView.as_view()),
    url(r'^logout/', apis.LogoutView.as_view()),
    url(r'^$', apis.UserListCreateView.as_view()),
    url(r'^membership/$', apis.MembershipCreateDestroyView.as_view())
]
