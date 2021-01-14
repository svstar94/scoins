from django.shortcuts import render

# Create your views here.
from .models import *

from django.views.generic import ListView, DetailView, View
import datetime
from django.contrib.auth.models import User

from django.shortcuts import render
from assetapp.models import Asset, id2ctg
from scoin.tools import get_model_fields

from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse

from crawler import *

from django.views.generic.edit import FormMixin
from bookapp.forms import AccountingCreationForm
# from sosin import py2sql
import requests
import json
import time

class HomeView(ListView, FormMixin):
    model = News
    template_name = 'homeapp/home.html'
    form_class = AccountingCreationForm
    context_object_name = 'news_list'
    # paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        # paginator = context['paginator']
        # page_numbers_range = 5
        # max_index = len(paginator.page_range)
        # page = self.request.GET.get('page')
        # current_page = int(page) if page else 1
        # start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        # end_index = start_index + page_numbers_range
        # if end_index >= max_index:
        #     end_index = max_index
        # page_range = paginator.page_range[start_index:end_index]
        # context['page_range'] = page_range

        labels = [id2ctg[field.name] for field in list(get_model_fields(Asset))[3:]]

        if self.request.user.is_authenticated:
            try:
                datas = Asset.objects.filter(id=self.request.user.asset_user.id).values()[0]
                pie_labels = []
                pie_datas = []
                for i, k in enumerate(datas):
                    if i < 3: continue
                    if datas[k]:
                        pie_labels.append(id2ctg[k])
                        pie_datas.append(datas[k])

                context['asset_list'] = Asset.objects.filter(id=self.request.user.asset_user.id).values()[0].values()
                context['data'] = pie_datas
                context['labels'] = pie_labels

            except:
                pass

            context['target_user'] = self.request.user

        return context

def coin_test_api(request):
    coin_name = request.POST['coin_name']
    print(coin_name)
    coin_search = CoinInfo.objects.filter(name=coin_name).values()
    print(coin_search)
    if len(coin_search) == 1:
        coin_idx = coin_search[0]['id']
        coin_list = [coin.sise for coin in Coin.objects.filter(code_id=coin_idx)]
        if len(coin_list) != 0:
            coin_labels = [coin.date.strftime('%Y%m%d') for coin in Coin.objects.filter(code_id=coin_idx)]
            data = {
                'check' : 1,
                'coin_list': coin_list,
                'coin_labels': coin_labels
            }
            return Response(data)
    data = {
        'check' : 0,
        'check_info': '코인 정보가 없습니다.'
    }
    return Response(data)

# def coin_test(code_id, coincode=None):
#     DB = py2sql.conn()
#     print('코인 크롤링 시작')
#     # 일별 비트코인 데이터
#     BASE_URL = 'https://api.bithumb.com/public/candlestick_trview/{}_KRW/24H'
#     r = requests.get(BASE_URL.format(coincode))
#     try:
#         res = json.loads(r.text)['data']
#     except:
#         print( '코인 데이터 가져오기 오류' )
#         return 'no data'
#     # 'c' = 종가
#     # 't' = 기준 시간
#     # 'v' = 거래량 (코인 개수 기준)
#     values = []
#     for i in range(len(res['t'])):
#         values.append('"%s"'%res['c'][i])
    
#     return values


class CoinAPIView(APIView):
    
    authentication_classes = []
    permission_classes = []

    def get(self, request): 
        coin_id = request.GET.get('coin_id', 'b')
        # print(coin_id)
        coin_search = CoinInfo.objects.filter(name=coin_id).values()
        # print(coin_search)
        # if len(coin_search) == 1:
        #     coin_idx = coin_search[0]['id']
        #     coin_list = [coin.sise for coin in Coin.objects.filter(code_id=coin_idx)]
        #     if len(coin_list) != 0:
        #         coin_labels = [coin.date.strftime('%Y%m%d') for coin in Coin.objects.filter(code_id=coin_idx)]
        #         data = {
        #             'check' : 1,
        #             'coin_list': coin_list,
        #             'coin_labels': coin_labels
        #         }
        #         return Response(data)
        data = {
            'check' : 0,
            'check_info': '코인 정보가 없습니다.',
            'coin_search' : coin_search,
        }
        return Response(data)


# from multiprocessing import Process
class StockAPIView(APIView):
    
    authentication_classes = []
    permission_classes = []

    def get(self, request): 
        stock_id = request.GET.get('stock_id', 's')
        stock_idx = StockInfo.objects.filter(name=stock_id).values()
        print(stock_id, stock_idx)

        if len(stock_idx) == 1:
            stock_idx = stock_idx[0]['id']
            stock_list = list(reversed([stock.sise for stock in Stock.objects.filter(code_id=stock_idx)]))
            # if len(stock_list) == 0:
            #     stock_code = StockInfo.objects.filter(name=stock_id).values()[0]['code']
            #     # 크롤링 하는 경우
            #     p = Process(target=stock_test, args=(stock_idx, stock_code, ))
            #     p.start()
            #     data = {
            #         'check' : 0,
            #         'check_info': '크롤링 중이거나 상폐된 주식입니다.'
            #     }
            #     return Response(data)
            stock_labels = [stock.date.strftime('%Y%m%d') for stock in Stock.objects.filter(code_id=stock_idx)]
            
            data = {
                'check' : 1,
                'stock_list': stock_list,
                'stock_labels': stock_labels
            }
            return Response(data)
        else:
            # 상장정보가 아예 없는 경우
            data = {
                'check' : 0,
                'check_info' : '상장 정보가 없습니다.'
            }
            return Response(data)

class SearchCoinAPIView(APIView):
    
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        keyword = request.GET.get('keyword', 'e')
        results = CoinInfo.objects.filter(name__startswith=keyword).values()
        data = {
            'sr': [r['name'] for r in results]
        }

        return Response(data)


class SearchStockAPIView(APIView):
    
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        keyword = request.GET.get('keyword', 'e')
        results = StockInfo.objects.filter(name__startswith=keyword).values()
        data = {
            'sr': [r['name'] for r in results]
        }

        return Response(data)