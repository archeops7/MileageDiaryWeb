# Generated by Django 3.0.8 on 2020-07-15 16:32

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('DiaryApp', '0002_auto_20200715_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='mileage',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
