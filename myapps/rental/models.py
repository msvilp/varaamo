"""
Rental models for equipment booking and management
"""
# pylint: disable=no-member
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal

# Create your models here.

RENTAL_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('active', 'Active'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
)

PAYMENT_STATUS_CHOICES = (
    ('unpaid', 'Unpaid'),
    ('paid', 'Paid'),
    ('refunded', 'Refunded'),
)


class Rental(models.Model):
    """Equipment rental booking"""
    # Basic information
    rental_user = models.ForeignKey(
        "users.RentalUser",
        on_delete=models.PROTECT,
        related_name="rentals"
    )
    equipment_item = models.ForeignKey(
        "equipment.EquipmentItem",
        on_delete=models.PROTECT,
        related_name="rentals"
    )

    # Rental period
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    # Pricing
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Status
    status = models.CharField(max_length=20, choices=RENTAL_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    # Admin fields
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Rental #{self.pk}: {self.rental_user.name} - {self.equipment_item.name}"

    def clean(self):
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError("Start date must be before end date")

        # Check for overlapping rentals
        if self.equipment_item and self.start_date and self.end_date:
            overlapping = Rental.objects.filter(
                equipment_item=self.equipment_item,
                start_date__lt=self.end_date,
                end_date__gt=self.start_date,
                status__in=['confirmed', 'active']
            ).exclude(pk=self.pk)

            if overlapping.exists():
                raise ValidationError("This equipment is already rented during the selected period")

    def save(self, *args, **kwargs):
        self.full_clean()
        # Calculate total price if not set
        if not self.total_price:
            self.calculate_total_price()
        super().save(*args, **kwargs)

    def calculate_total_price(self):
        """Calculate total price based on rental period and equipment price group"""
        if not self.start_date or not self.end_date or not self.equipment_item.price_group:
            return

        duration = self.end_date - self.start_date
        hours = duration.total_seconds() / 3600

        # Determine if user is member
        is_member = self.rental_user.group.name.lower() == 'member'

        # Get the most appropriate price rule from equipment's price group
        price_rules = self.equipment_item.price_group.rules.all()

        # Determine best price rule based on duration
        if hours <= 1:
            price_rule = price_rules.filter(time='hour').first()
        elif hours <= 24:
            price_rule = price_rules.filter(time='day').first() or price_rules.filter(time='hour').first()
        elif hours <= 48:
            price_rule = price_rules.filter(time='weekend').first() or price_rules.filter(time='day').first()
        else:
            price_rule = price_rules.filter(time='week').first() or price_rules.filter(time='weekend').first()

        if not price_rule:
            price_rule = price_rules.first()  # Fallback to any rule

        if not price_rule:
            return

        base_price = price_rule.member_price if is_member else price_rule.customer_price

        # Calculate based on price rule time type
        if price_rule.time == 'hour':
            self.total_price = base_price * Decimal(str(max(1, int(hours))))
        elif price_rule.time == 'day':
            days = max(1, int(hours / 24))
            self.total_price = base_price * Decimal(str(days))
        elif price_rule.time == 'weekend':
            weekends = max(1, int(hours / (48)))  # 48 hours = weekend
            self.total_price = base_price * Decimal(str(weekends))
        elif price_rule.time == 'week':
            weeks = max(1, int(hours / (24 * 7)))
            self.total_price = base_price * Decimal(str(weeks))
        else:
            self.total_price = base_price

    def cancel_rental(self, reason=""):
        """Cancel the rental"""
        self.status = 'cancelled'
        self.cancelled_at = timezone.now()
        self.cancellation_reason = reason
        self.save()

    def mark_as_paid(self):
        """Mark rental as paid"""
        self.payment_status = 'paid'
        self.paid_at = timezone.now()
        self.save()

    def is_active(self):
        """Check if rental is currently active"""
        now = timezone.now()
        return (self.status == 'active' and
                self.start_date <= now <= self.end_date)

    def duration_hours(self):
        """Get rental duration in hours"""
        if self.start_date and self.end_date:
            duration = self.end_date - self.start_date
            return duration.total_seconds() / 3600
        return 0

    class Meta:
        verbose_name = "rental"
        verbose_name_plural = "rentals"
        ordering = ['-created_at']


class RentalExtension(models.Model):
    """Extension of existing rental"""
    rental = models.ForeignKey(
        Rental,
        on_delete=models.CASCADE,
        related_name="extensions"
    )
    original_end_date = models.DateTimeField()
    new_end_date = models.DateTimeField()
    additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Extension for Rental #{self.rental.pk}"

    class Meta:
        verbose_name = "rental extension"
        verbose_name_plural = "rental extensions"
        ordering = ['-created_at']
