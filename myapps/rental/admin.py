from django.contrib import admin
from django.contrib import messages

from . import models

# Register your models here.


class RentalExtensionInline(admin.TabularInline):
    model = models.RentalExtension
    extra = 0
    readonly_fields = ('original_end_date', 'created_at')


@admin.register(models.Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'rental_user', 'equipment_item_display', 'start_date', 'end_date',
        'total_price', 'status', 'payment_status', 'created_at'
    )
    list_filter = (
        'status', 'payment_status', 'created_at', 'start_date',
        'equipment_item__equipment_class', 'rental_user__group'
    )
    search_fields = (
        'rental_user__name', 'rental_user__email',
        'equipment_item__name', 'equipment_item__number'
    )
    readonly_fields = (
        'created_at', 'updated_at', 'cancelled_at', 'paid_at',
        'total_price_display', 'duration_display'
    )
    list_select_related = ('rental_user', 'equipment_item')
    autocomplete_fields = ('rental_user', 'equipment_item')
    inlines = [RentalExtensionInline]
    date_hierarchy = 'start_date'
    list_per_page = 25

    fieldsets = (
        ('Rental Information', {
            'fields': (
                'rental_user', 'equipment_item', 'start_date', 'end_date',
                'duration_display'
            ),
            'description': 'Basic rental information and scheduling'
        }),
        ('Pricing', {
            'fields': ('total_price_display', 'total_price'),
            'description': 'Price will be calculated automatically based on duration and equipment price group'
        }),
        ('Status', {
            'fields': ('status', 'payment_status')
        }),
        ('Notes & Admin', {
            'fields': ('notes', 'cancellation_reason'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'cancelled_at', 'paid_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['mark_as_paid', 'cancel_rentals', 'confirm_rentals']

    def equipment_item_display(self, obj):
        return f"{obj.equipment_item.equipment_class.name} - {obj.equipment_item.name}"
    equipment_item_display.short_description = 'Equipment'
    equipment_item_display.admin_order_field = 'equipment_item__name'

    def total_price_display(self, obj):
        if obj.total_price:
            return f"€{obj.total_price}"
        return "-"
    total_price_display.short_description = 'Total Price'

    def duration_display(self, obj):
        hours = obj.duration_hours()
        if hours:
            if hours < 24:
                return f"{hours:.1f} hours"
            else:
                days = hours / 24
                return f"{days:.1f} days"
        return "-"
    duration_display.short_description = 'Duration'

    def mark_as_paid(self, request, queryset):
        updated = 0
        for rental in queryset:
            if rental.payment_status != 'paid':
                rental.mark_as_paid()
                updated += 1

        self.message_user(
            request,
            f"{updated} rental(s) marked as paid.",
            messages.SUCCESS
        )
    mark_as_paid.short_description = "Mark selected rentals as paid"

    def cancel_rentals(self, request, queryset):
        updated = 0
        for rental in queryset:
            if rental.status not in ['cancelled', 'completed']:
                rental.cancel_rental("Cancelled by admin")
                updated += 1

        self.message_user(
            request,
            f"{updated} rental(s) cancelled.",
            messages.SUCCESS
        )
    cancel_rentals.short_description = "Cancel selected rentals"

    def confirm_rentals(self, request, queryset):
        updated = 0
        for rental in queryset:
            if rental.status == 'pending':
                rental.status = 'confirmed'
                rental.save()
                updated += 1

        self.message_user(
            request,
            f"{updated} rental(s) confirmed.",
            messages.SUCCESS
        )
    confirm_rentals.short_description = "Confirm selected rentals"

    def save_model(self, request, obj, form, change):
        # Auto-calculate price if not set
        if not obj.total_price:
            obj.calculate_total_price()
        super().save_model(request, obj, form, change)


@admin.register(models.RentalExtension)
class RentalExtensionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'rental', 'original_end_date', 'new_end_date',
        'additional_price', 'created_at'
    )
    list_filter = ('created_at', 'original_end_date', 'new_end_date')
    search_fields = ('rental__rental_user__name', 'rental__equipment_item__name')
    readonly_fields = ('created_at',)
    autocomplete_fields = ('rental',)
    date_hierarchy = 'created_at'

