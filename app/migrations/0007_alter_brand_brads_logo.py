# Generated by Django 4.1.7 on 2023-03-16 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_brand_brads_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='Brads_Logo',
            field=models.ImageField(null=True, upload_to='Brands_Logo/'),
        ),
    ]