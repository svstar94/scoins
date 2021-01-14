
from .views import *
from django.urls import path

app_name = 'homeapp'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    # path('news/', NewsView.as_view(), name='news')
    path('api/coin/', coin_test_api, name='coin_sise_api'),
    path('api/stock/', StockAPIView.as_view(), name='stock_sise_api'),
    path('api/coin_search/', SearchCoinAPIView.as_view(), name='coin_search_api'),
    path('api/stock_search/', SearchStockAPIView.as_view(), name='stock_search_api'),
]
