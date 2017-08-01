from django.contrib import admin

from .models import MyGroup


class GroupAdmin(admin.ModelAdmin):
    pass

admin.site.register(MyGroup, GroupAdmin)