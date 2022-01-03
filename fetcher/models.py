from django.db import models


# Create your models here.
class Business(models.Model):
    name = models.CharField(max_length=150)
    registry_code = models.IntegerField()
    legal_form = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
    registered_date = models.DateField()
    financial_year = models.CharField(max_length=150)
    other = models.JSONField()


class Person(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    role = models.CharField(max_length=250)


class Activity(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    type = models.CharField(max_length=150)
    area = models.CharField(max_length=250)
    EMTAK_code = models.CharField(max_length=250)
    NACE_code = models.CharField(max_length=250)
    source = models.CharField(max_length=250)


