"""
# Varaamo - Equipment Management Models
# This module defines models for managing equipment, including price rules, classes, groups, and individual items."""
import uuid

from django.db import models


PRICE_RULE_OPTIONS = (
    ('hour', 'Hour'),
    ('day', 'Day'),
    ('weekend', 'Weekend'),
    ('week', 'Week'),
)


class EquipmentPriceRule(models.Model):
    """Price rule for equipment"""
    customer_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    member_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    time = models.CharField(max_length=10, choices=PRICE_RULE_OPTIONS)

    price_group = models.ForeignKey("EquipmentPriceGroup", on_delete=models.CASCADE, related_name="rules")

    def __str__(self):
        return f"{self.__class__.__name__} #{self.pk}: {self.customer_price} / {self.member_price} / {self.time}"

    class Meta:
        verbose_name = "equipment price rule"
        verbose_name_plural = "equipment price rules"


class EquipmentPriceGroup(models.Model):
    """Price group for equipment"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, editable=False)

    def __str__(self):
        return f"{self.__class__.__name__} #{self.pk}: {self.name}"

    class Meta:
        verbose_name = "equipment price group"
        verbose_name_plural = "equipment price groups"


class EquipmentClass(models.Model):
    """Class or type of equipment"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)
    code = models.CharField(max_length=10, blank=True)
    visible = models.BooleanField(default=True)
    rentable = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.__class__.__name__} #{self.pk}: {self.name}"

    class Meta:
        verbose_name = "equipment class"
        verbose_name_plural = "equipment classes"


class EquipmentGroup(models.Model):
    """Group of similar equipment"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, editable=False)
    image = models.ImageField(upload_to="equipment_images/", blank=True)

    def __str__(self):
        return f"{self.__class__.__name__} #{self.pk}: {self.name}"

    class Meta:
        verbose_name = "equipment group"
        verbose_name_plural = "equipment groups"


class EquipmentItem(models.Model):
    """Equipment item or multiple identical items"""
    name = models.CharField(max_length=200)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=100)
    short_slug = models.SlugField(max_length=10)
    number = models.CharField(max_length=10, blank=True)
    visible = models.BooleanField(default=True)
    rentable = models.BooleanField(default=True)
    count = models.IntegerField(default=1, null=False, blank=False)

    image = models.ImageField(upload_to="equipment_images/", blank=True)

    equipment_class = models.ForeignKey(
        "EquipmentClass",
        on_delete=models.PROTECT,
        related_name="equipment"
    )
    equipment_group = models.ForeignKey(
        "EquipmentGroup",
        on_delete=models.PROTECT,
        related_name="items",
        null=True,
        blank=True,
    )
    price_group = models.ForeignKey(
        "EquipmentPriceGroup",
        on_delete=models.PROTECT,
        related_name="items",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.__class__.__name__} #{self.pk}: {self.equipment_class.name} / {self.name}"

    class Meta:
        verbose_name = "equipment item"
        verbose_name_plural = "equipment items"
