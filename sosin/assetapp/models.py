from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
# 현재 보유 자산 DB
class Asset(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='asset_user')
    date = models.DateTimeField('DATE', default=timezone.now) # 시작 날짜
    freedps = models.IntegerField('FREEDPS', blank=True, null=True) # 자유입출금
    stock = models.IntegerField('STOCK', blank=True, null=True) # 주식
    installment = models.IntegerField('INSTALLMENT', blank=True, null=True) # 적금
    house_sbsc = models.IntegerField('HOUSE_SBSC', blank=True, null=True) # 주택청약
    cma = models.IntegerField('CMA', blank=True, null=True) # CMA
    invest = models.IntegerField('INVEST', blank=True, null=True) # 투자 - 펀드, 연금
    house = models.IntegerField('HOUSE', blank=True, null=True) # 부동산
    debt = models.IntegerField('DEPT', blank=True, null=True) # 부채

    # def __str__(self):
    #     return '가입날짜: %s 자유입출금: %s 주식: %s 적금: %s 주택청약: %s CMA: %s 투자: %s 부동산: %s 부채: %s'%(
    #         self.date, self.freedps, self.stock, self.installment, self.house_sbsc, self.cma, self.invest, self.house, self.debt)

id2ctg = {
    'freedps' : '자유입출금', 'stock' : '주식', 'installment' : '적금', 'house_sbsc' : '주택청약', 'cma' : 'CMA', 'invest' : '투자', 'house' : '부동산', 'debt' : '부채'
}