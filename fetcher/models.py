from django.db import models


# Create your models here.
class Business(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    registry_code = models.CharField(max_length=150, blank=True, null=True)
    legal_form = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=150, blank=True, null=True)
    registered_date = models.CharField(max_length=150, blank=True, null=True)
    financial_year = models.CharField(max_length=150, blank=True, null=True)
    url = models.CharField(max_length=1600, unique=True)
    complete = models.BooleanField(default=False)
    in_process = models.BooleanField(default=False)
    vat_number = models.CharField(max_length=120, blank=True, null=True)
    vat_period = models.CharField(max_length=120, blank=True, null=True)
    state_taxes = models.CharField(max_length=120, blank=True, null=True)
    taxes_on_workforce = models.CharField(max_length=120, blank=True, null=True)
    taxable_turnover = models.CharField(max_length=210, blank=True, null=True)
    number_of_employees = models.CharField(max_length=3, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    get_on_next_fetch = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(blank=True, null=True)

    @property
    def representation(self):
        return Person.objects.filter(business=self)

    @property
    def activity(self):
        return Activity.objects.filter(business=self)


class Person(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=True, null=True)
    role = models.CharField(max_length=250, blank=True, null=True)
    person_id = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return f"{self.name} -- {self.role} -- {self.person_id}"


class Activity(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    area = models.CharField(max_length=250, blank=True, null=True)
    EMTAK_code = models.CharField(max_length=250, blank=True, null=True)
    NACE_code = models.CharField(max_length=250, blank=True, null=True)
    source = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.area


class Page(models.Model):
    page = models.IntegerField()
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.page} --- Status: {'deactive' if self.finished else 'active'}"


class Proxy(models.Model):
    proxy = models.CharField(max_length=1200)
    last_used_date = models.DateTimeField(auto_now_add=True)


class URL(models.Model):
    url = models.CharField(max_length=2000)
    failed = models.BooleanField(default=False)

    def __str__(self):
        return f"Status: {'deactive' if self.failed else 'active'}"
