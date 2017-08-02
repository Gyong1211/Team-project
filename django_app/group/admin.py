from django.contrib import admin

from .models import MyGroup, GroupTag, Membership


class GroupAdmin(admin.ModelAdmin):
    pass


admin.site.register(MyGroup, GroupAdmin)


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(GroupTag, TagAdmin)


class MembershipAdmin(admin.ModelAdmin):
    pass


admin.site.register(Membership, MembershipAdmin)
