# Generated by Django 4.1.7 on 2023-03-25 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_Name', models.CharField(max_length=20)),
                ('User_Email', models.EmailField(max_length=254, null=True)),
                ('User_Password', models.CharField(max_length=20, null=True)),
            ],
        ),
    ]
