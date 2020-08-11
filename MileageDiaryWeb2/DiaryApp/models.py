import datetime

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.contrib.auth import get_user_model

# Create your models here.
def check_km(value):
    if value < 0 or value > 1000:
        raise ValidationError('正しい距離(0~1000km)を入力してください。')
def check_litter(value):
    if value < 0 or value > 100:
        raise ValidationError('正しい量(0~100L)を入力してください。')
def check_price(value):
    if value < 0 or value > 300:
        raise ValidationError('正しい単価(0~300円)を入力してください。')

class Log(models.Model):
    km = models.DecimalField(max_digits=6, decimal_places=2, validators=[check_km])
    litter = models.DecimalField(max_digits=5, decimal_places=2, validators=[check_litter])
    price = models.IntegerField(validators=[check_price])
    trip_memo = models.CharField(max_length=100, validators=[MaxLengthValidator(100, '100文字以内にしてください。')])
    updated_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    
    def __str__(self):
        return self.trip_memo
    
    def was_published_recently(self):
        return self.updated_at >= timezone.now() - datetime.timedelta(days=1)