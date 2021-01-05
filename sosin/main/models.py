from django.db import models
from django.utils import timezone

# Create your models here.
# 주가 DB
class Stocks(models.Model):
    date = models.DateTimeField('DATE', default=timezone.now) # 날짜
    code = models.CharField('CODE', blank=False, max_length=6)
    name = models.CharField('NAME', blank=False, max_length=20)
    sise = models.PositiveIntegerField('SISE', blank=False)
    amount = models.PositiveBigIntegerField('AMOUNT', blank=False)

# 코인 DB
class Coins(models.Model):
    date = models.DateTimeField('DATE', default=timezone.now) # 날짜
    code = models.CharField('CODE', blank=False, max_length=3)
    name = models.CharField('NAME', blank=False, max_length=15)
    sise = models.PositiveIntegerField('SISE', blank=False)
    amount = models.FloatField('AMOUNT', blank=False)

# 뉴스 DB
class News(models.Model):
    date = models.DateTimeField('DATE', default=timezone.now) # 날짜
    title = models.CharField('TITLE', blank=False, max_length=100)
    content = models.TextField('CONTENT', blank=True)
    publisher = models.CharField('PUBLISHER', blank=False, max_length=8)
    url = models.URLField('URL', blank=True)
