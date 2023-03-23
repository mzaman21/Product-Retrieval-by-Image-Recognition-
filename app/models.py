from django.db import models

# Create your models here.
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
