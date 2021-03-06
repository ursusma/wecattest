from django.db import models
from django.utils import timezone

# Create your models here.

class Product(models.Model):
    Total = models.CharField(max_length=30,null=True)

    def __str__(self):
        return self.Toltal

class Detailed(models.Model):
    SurfaceName = models.CharField(max_length=30,null=True)
    Img = models.ImageField(null=True,blank=True,upload_to="img")
    Introduce = models.TextField(null=True)
    Price = models.FloatField(null=True)
    ProId = models.ForeignKey('Product')

    def __str__(self):
        return self.SurfaceName

class WxText(models.Model):
    title = models.CharField(max_length=30,null=True)
    img = models.ImageField(null=True,blank=True,upload_to="img")
    text =models.TextField(null=True)

    def __str__(self):
        return self.title
