from django.contrib import admin

from . import models


class RentalUserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "group_name", "admin")
    list_filter = ("group", "admin")
    search_fields = ("name", "email")
    autocomplete_fields = ("group",)
    
    def group_name(self, model):
        return model.group.name
    group_name.short_description = "Group"
    group_name.admin_order_field = "group__name"


class RentalGroupsAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(models.RentalUser, RentalUserAdmin)
admin.site.register(models.RentalUserGroup, RentalGroupsAdmin)