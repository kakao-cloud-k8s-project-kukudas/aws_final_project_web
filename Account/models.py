from django.db import models
import datetime
# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key = True)
    company_name = models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    pw=models.CharField(max_length=300) # 암호화로 인해 긺
    worker_min = models.CharField(max_length=100)
    worker_max = models.CharField(max_length=100)
    pod_min = models.CharField(max_length=100)
    pod_max = models.CharField(max_length=100)
    lb_address = models.CharField(null = True, max_length=100)
    class Meta:
        db_table=''