from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
# 유저 자산 DB
class Assets(models.Model):
    userid = models.CharField('USERID', max_length=100, blank=False) # 유저 고유 아이디
    date = models.DateTimeField('DATE', default=timezone.now) # 시작 날짜
    freedps = models.IntegerField('FREEDPS', blank=True) # 자유입출금
    stock = models.IntegerField('STOCK', blank=True) # 주식
    installment = models.IntegerField('INSTALLMENT', blank=True) # 적금
    house_sbsc = models.IntegerField('HOUSE_SBSC', blank=True) # 주택청약
    cma = models.IntegerField('CMA', blank=True) # CMA
    invest = models.IntegerField('INVEST', blank=True) # 투자 - 펀드, 연금
    house = models.IntegerField('HOUSE', blank=True) # 부동산
    debt = models.IntegerField('DEPT', blank=True) # 부채

    def __str__(self):
        return '%s : 가입날짜 : %s'%(self.userid, self.date)
    