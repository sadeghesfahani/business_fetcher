from django.db import models


# Create your models here.
class Business(models.Model):
    name = models.CharField(max_length=150)
    registry_code = models.IntegerField(blank=True,null=True)
    legal_form = models.CharField(max_length=150,blank=True,null=True)
    status = models.CharField(max_length=150,blank=True,null=True)
    registered_date = models.DateField(blank=True,null=True)
    financial_year = models.CharField(max_length=150,blank=True,null=True)
    other = models.JSONField(blank=True,null=True)
    url = models.CharField(max_length=1600, unique=True)

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


class Page(models.Model):
    page = models.SmallIntegerField()