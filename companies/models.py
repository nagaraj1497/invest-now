from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    share_price = models.DecimalField(decimal_places=2, max_digits=20)

    class Meta:
        db_table = "companies"

    def __str__(self):
        return self.name

class Investment(models.Model):
    invest_id = models.AutoField(primary_key=True)
    funds = models.DecimalField(max_digits=20,decimal_places=2)
    no_shares = models.IntegerField(null=False, default=0)
    invest_amount = models.DecimalField(max_digits=20,decimal_places=2)
    total_balance = models.DecimalField(max_digits=20,decimal_places=2)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "investment"

