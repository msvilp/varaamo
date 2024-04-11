from django.contrib import admin

from . import models

class PriceRuleInline(admin.TabularInline):
    model = models.EquipmentPriceRule

class PriceGroupAdmin(admin.ModelAdmin):
    inlines = [PriceRuleInline]

class EquipmentClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'visible', 'rentable')


class EquipmentGroupAdmin(admin.ModelAdmin):
    list_display = ('name', )


class EquipmentItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'equipment_class_name', 'count', 'equipment_group', 'visible', 'rentable')

    def equipment_class_name(self, equipment):
        return equipment.equipment_class.name


admin.site.register(models.EquipmentClass, EquipmentClassAdmin)
admin.site.register(models.EquipmentGroup, EquipmentGroupAdmin)
admin.site.register(models.EquipmentItem, EquipmentItemAdmin)
admin.site.register(models.EquipmentPriceGroup, PriceGroupAdmin)