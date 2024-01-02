
from django.db import models

class Store(models.Model):
    Store = models.CharField(max_length=4)
    IP = models.CharField(max_length=17, unique=True)
    Store_Name = models.CharField(max_length=40, null=True)
    Store_Name_AR = models.CharField(max_length=80, null=True)
    RegKey = models.CharField(max_length=300, null=True)
    Number_Range = models.CharField(max_length=4)
    Region_ID = models.IntegerField(null=True)
    Delivery = models.IntegerField(null=True)
    isTouristic = models.BooleanField(null=True)
    NetworkType = models.CharField(max_length=1, null=True)
    Store_Location = models.CharField(max_length=50, null=True)
    Status = models.IntegerField(null=True, default=1)

    def __str__(self):
        return self.Store
