from csv import list_dialects
from django.contrib import admin

from . import models


class RentalUserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "group_name", "admin")

    def group_name(self, model):
        return model.group.name


class RentalGroupsAdmin(admin.ModelAdmin):
    list_display = ("name", )


admin.site.register(models.RentalUser, RentalUserAdmin)
admin.site.register(models.RentalUserGroup, RentalGroupsAdmin)