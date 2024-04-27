from django.db import models
#from django.contrib.gis.db import models


# Create your models here.
# test mysqlconnect
class Register(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)


# 把移动感知端传来的数据存入数据库
class LocationData(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    signal_strength = models.FloatField()
    is_aggr = models.BooleanField(default=False)
    is_ask = models.BooleanField(default=False)
    Network = models.CharField(max_length=10,default=None, null=True)
    Operator = models.FloatField()
    Users= models.CharField(max_length=50,default=None, null=True)
    obj = models.FloatField()
    rsrq = models.FloatField()
    rssnr = models.FloatField()
    Time = models.CharField(max_length=30,default=None,null=True)

    def __str__(self):
        return f'Latitude: {self.latitude}, Longitude: {self.longitude}'




