from django.db import models

# Create your models here.
from django.utils.text import slugify


class Brand(models.Model):
    Brand_id = models.AutoField
    Brand_Name = models.CharField(max_length=20)
    Brand_Email = models.EmailField(null=True)
    Brand_Password = models.CharField(max_length=20,null=True)
    Brand_Address = models.TextField(null=True)
    Brand_City = models.CharField(max_length=25,null=True)
    Brand_State = models.CharField(max_length=20,null=True)
    Brand_Zip = models.CharField(max_length=15,null=True)
    Brands_Logo = models.ImageField(upload_to='Brands_Logo/',null=True)

    def __str__(self):
        return self.Brand_Name


class Product(models.Model):
    Product_Name = models.CharField(max_length=40)
    Product_Price = models.CharField(max_length=20)
    Product_Category = models.CharField(max_length=20)
    Product_Description = models.TextField(max_length=50)
    Product_Stock = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, null=True, blank=True)
    Product_Brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def save(self , *args , **kwargs):
        self.slug = slugify(self.Product_Name)
        super(Product ,self).save(*args , **kwargs)
    def __str__(self):
        return self.Product_Name

class PImage(models.Model):
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Product_Image = models.ImageField(upload_to='Product_Images/')
    def __str__(self):
        return self.Product.Product_Name