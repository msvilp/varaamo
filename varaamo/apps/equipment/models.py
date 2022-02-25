from django.db import models

import uuid


class EquipmentClass(models.Model):
    """Class or type of equipment"""
    name = models.CharField(max_length=200)
    visible = models.BooleanField(default=True)
    rentable = models.BooleanField(default=True)


class EquipmentGroup(models.Model):
    """Group of similar equipment"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, editable=False)


class EquipmentItem(models.Model):
    """Equipment item or multiple identical items"""
    name = models.CharField(max_length=200)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=100, editable=False)
    short_slug = models.SlugField(max_length=10, editable=False)
    visible = models.BooleanField(default=True)
    rentable = models.BooleanField(default=True)

    image = models.ImageField(upload_to="equipment_images/")

    equipment_class = models.ForeignKey(
        "EquipmentClass",
        on_delete=models.PROTECT,
        related_name="equipment"
    )
    equipment_group = models.ForeignKey(
        "EquipmentGroup",
        on_delete=models.CASCADE,
        related_name="items",
        null=True,
        blank=True,
    )

