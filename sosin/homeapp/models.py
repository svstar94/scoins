from django.db import models
from django.utils import timezone

# Create your models here.


# 주가 DB
class StockInfo(models.Model):
    code = models.CharField('CODE', blank=False, max_length=6)
    name = models.CharField('NAME', blank=False, max_length=20)

# code_id 가 stockinfo의 id값임 (primary key, not stock code(6))
class Stock(models.Model):
    code = models.ForeignKey(StockInfo, on_delete=models.SET_NULL, related_name='stock', null=True)
    date = models.DateTimeField('DATE', default=timezone.now) # 날짜
    sise = models.PositiveIntegerField('SISE', blank=False)
    amount = models.PositiveBigIntegerField('AMOUNT', blank=False)

# 코인 DB
class CoinInfo(models.Model):
    code = models.CharField('CODE', blank=False, max_length=3)
    name = models.CharField('NAME', blank=False, max_length=15)

# code -> code_id로 들어가있음 (primary key, not coin code(3))
class Coin(models.Model):
    code = models.ForeignKey(CoinInfo, on_delete=models.SET_NULL, related_name='coin', null=True)
    date = models.DateTimeField('DATE', default=timezone.now) # 날짜
    sise = models.PositiveIntegerField('SISE', blank=False)
    amount = models.FloatField('AMOUNT', blank=False)

# 뉴스 DB
class News(models.Model):
    date = models.DateTimeField('DATE', default=timezone.now) # 날짜
    title = models.CharField('TITLE', blank=False, max_length=100)
    content = models.TextField('CONTENT', blank=True)
    publisher = models.CharField('PUBLISHER', blank=False, max_length=8)
    url = models.URLField('URL', blank=True)