from django.contrib import admin
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from . import models

class PriceRuleInline(admin.TabularInline):
    model = models.EquipmentPriceRule

class PriceGroupAdmin(admin.ModelAdmin):
    inlines = [PriceRuleInline]
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

class EquipmentClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'slug', 'visible', 'rentable')
    list_filter = ('visible', 'rentable')
    search_fields = ('name', 'code', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('visible', 'rentable')
    ordering = ('name',)


class EquipmentGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'has_image')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'


class EquipmentItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'equipment_class_name', 'number', 'short_slug', 'count', 'equipment_group', 'visible', 'rentable')
    list_filter = ('equipment_class', 'equipment_group', 'visible', 'rentable')
    search_fields = ('name', 'number', 'short_slug')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('visible', 'rentable', 'count')
    ordering = ('equipment_class__name', 'name')
    list_select_related = ('equipment_class', 'equipment_group', 'price_group')
    autocomplete_fields = ('equipment_class', 'equipment_group', 'price_group')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'short_slug', 'number', 'count')
        }),
        ('Classification', {
            'fields': ('equipment_class', 'equipment_group', 'price_group')
        }),
        ('Settings', {
            'fields': ('visible', 'rentable', 'image')
        }),
    )
    
    def equipment_class_name(self, obj):
        return obj.equipment_class.name
    equipment_class_name.short_description = 'Equipment Class'
    equipment_class_name.admin_order_field = 'equipment_class__name'
    
    def save_model(self, request, obj, form, change):
        # Auto-generate short_slug if not provided
        if not obj.short_slug:
            base_slug = slugify(obj.name)[:10]
            obj.short_slug = base_slug
            
        # Ensure short_slug is unique
        counter = 1
        original_short_slug = obj.short_slug
        while models.EquipmentItem.objects.filter(short_slug=obj.short_slug).exclude(pk=obj.pk).exists():  # pylint: disable=no-member
            obj.short_slug = f"{original_short_slug[:8]}{counter:02d}"
            counter += 1
            if counter > 99:  # Prevent infinite loop
                raise ValidationError("Unable to generate unique short slug")
                
        super().save_model(request, obj, form, change)

admin.site.register(models.EquipmentClass, EquipmentClassAdmin)
admin.site.register(models.EquipmentGroup, EquipmentGroupAdmin)
admin.site.register(models.EquipmentItem, EquipmentItemAdmin)
admin.site.register(models.EquipmentPriceGroup, PriceGroupAdmin)
