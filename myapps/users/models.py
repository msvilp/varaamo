import uuid
from datetime import datetime, timedelta

from django.db import models

# Create your models here.

class RentalUserGroup(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return f"{self.__class__.__name__} #{self.pk}: {self.name}"


class RentalUser(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    group = models.ForeignKey("RentalUserGroup", on_delete=models.PROTECT)
    admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


def default_expiry_date():
    return datetime.now + timedelta(hours=2)

class RentalUserLogin(models.Model):
    user = models.ForeignKey("RentalUser", on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    expires = models.DateTimeField(default=default_expiry_date)

    def is_active(self):
        return self.expires < datetime.datetime.now

    def __str__(self):
        return f"{self.__class__.__name__} #{self.pk}: expires {self.expires}"