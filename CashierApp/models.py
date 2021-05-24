from django.db import models

# Create your models here.


class Cashier(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    block = models.CharField(max_length=255)


class Resident(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    apartment = models.IntegerField()
    cashier_id = models.ForeignKey(Cashier, on_delete=models.CASCADE)


class Payment(models.Model):
    type = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    amount = models.IntegerField()
    date = models.DateField()
    resident_id = models.ForeignKey(Resident, on_delete=models.CASCADE)


