# Generated by Django 4.1.7 on 2023-04-29 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_order_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='dispatch_status',
            field=models.BooleanField(default=False),
        ),
    ]
