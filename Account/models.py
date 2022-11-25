from django.db import models
import datetime
# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class User_info(models.Model):
    id = models.AutoField(primary_key = True)
    company_name = models.CharField(max_length=100)
    # company_name = models.CharField(primary_key = True, max_length=100)
    company_initial = models.CharField(max_length=3)
    date=models.CharField(max_length=100)
    pw=models.CharField(max_length=128) # 암호화로 인해 긺
    worker_min = models.CharField(max_length=100)
    worker_max = models.CharField(max_length=100)
    pod_min = models.CharField(max_length=100)
    pod_max = models.CharField(max_length=100)
    lb_address = models.CharField(null = True, max_length=100)
    cluster_exist = models.BooleanField(default=False)