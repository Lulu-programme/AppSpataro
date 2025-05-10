from django.contrib.auth.models import AbstractUser
from django.db import models


class Truck(models.Model):
    license = models.CharField(max_length=50, null=True, blank=True)
    technical = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    tachograph = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    maintenance = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    adr = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return self.license


class Account(AbstractUser):

    truck = models.CharField(max_length=50, null=True, blank=True)
    drive_license = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    adr_license = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    driver_card = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    sector = models.CharField(max_length=50, blank=True, null=True)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name()
