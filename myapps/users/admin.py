from csv import list_dialects
from django.contrib import admin

from . import models

class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "group_name", "admin")

    def group_name(self, model):
        return model.group.name

class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", )

admin.site.register(models.RentalUser, UserAdmin)
admin.site.register(models.RentalUserGroup, GroupAdmin)