from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^api/member/', include('member.urls')),
    # url(r'^api/group/', include('group.urls')),
    # url(r'^api/post/', include('post.urls')),
    url(r'^admin/', admin.site.urls),
]
