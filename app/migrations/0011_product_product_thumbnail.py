# Generated by Django 4.1.7 on 2023-03-25 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_remove_product_product_image_pimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Product_Thumbnail',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
