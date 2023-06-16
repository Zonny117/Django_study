from django.db import models


# Create your models here.
class Excel(models.Model):
    product_id = models.IntegerField()
    name = models.CharField(max_length=10)
    product = models.CharField(max_length=10)
