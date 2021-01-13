from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Accounting(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='book', null=True)
    date = models.DateField('DATE', default=timezone.now)
    iore = models.BooleanField('IORE', blank=False)
    big_category = models.CharField('BIG_CATEGORY',blank=True, null=True, max_length=10)
    mid_category = models.CharField('MID_CATEGORY', blank=True, null=True, max_length=10)
    sma_category = models.CharField('SMA_CATEGORY', blank=True, null=True, max_length=10)

    memo = models.CharField('MEMO', max_length=255, blank=True)
    amount = models.PositiveBigIntegerField('AMOUNT', blank=False)
