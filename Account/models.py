from django.db import models
import datetime
# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class User_info(models.Model):
    company_name = models.CharField(primary_key = True, max_length=100)
    company_initial = models.CharField(max_length=3)
    date=models.CharField(max_length=10)
    lb_address = models.CharField(null = True, max_length=100)
    rds_address = models.CharField(null = True, max_length=100)
    grafana_address = models.CharField(null = True, max_length=150)
    cluster_exist = models.BooleanField(default=False)