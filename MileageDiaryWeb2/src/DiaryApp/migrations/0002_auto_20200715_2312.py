# Generated by Django 3.0.8 on 2020-07-15 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DiaryApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
