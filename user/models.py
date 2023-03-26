from django.db import models

# Create your models here.
class User(models.Model):
    User_id = models.AutoField
    User_Name = models.CharField(max_length=20)
    User_Email = models.EmailField(null=True)
    User_Password = models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.User_Name
