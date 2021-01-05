import requests
import json
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import py2sql
import MySQLdb
import time

COM_DATE = '25569'

# Table Name : 'main_coins'
# 날짜, 코드, 이름, 종가, 체결량
def coin(DB, coincode=None):
    print('코인 크롤링 시작')
    coin_columns = 'date, code, name, sise, amount'
    # 일별 비트코인 데이터
    BASE_URL = 'https://api.bithumb.com/public/candlestick_trview/BTC_KRW/24H'
    r = requests.get(BASE_URL)
    res = json.loads(r.text)['data']
    # 'c' = 종가
    # 't' = 기준 시간
    # 'v' = 거래량 (코인 개수 기준)

    for i in range(len(res['t'])):
        values = []
        t = time.gmtime(int(res['t'][i])/1000)

        values.append('"%s-%s-%s"'%(t.tm_year, t.tm_mon, t.tm_mday))
        values.append('"%s"'%'BTC')
        values.append('"%s"'%'비트코인')
        values.append('"%s"'%res['c'][i])
        values.append('"%.2f"'%float(res['v'][i]))

        # db에 입력
        try: py2sql.insert(DB, 'main_coins', coin_columns, ','.join(values))
        except: pass

    # pd.DataFrame(res).to_csv('temp.csv')

# Table Name : 'main_stocks'
def stock(DB, stockcode=None):
    print('주식 크롤링 시작')
    stock_columns = 'date, code, name, sise, amount'
    BASE_URL = 'https://finance.naver.com/item/sise_day.nhn?code={}&page={}'
    stockcode='005930'

    for i in range(1, 671):
        print('%s page 크롤링 중...'%i)
        r = requests.get(BASE_URL.format(stockcode, i))
        sp = BeautifulSoup(r.text, 'html.parser')
        results = sp.select('tr')
        for i, result in enumerate(results):
            if i in [2,3,4,5,6,10,11,12,13,14]:
                stocks = result.select('td')
                values = []
                # yyyy-mm-dd hh:mm:ss
                values.append('"%s"'%stocks[0].text.replace('.', '-'))
                values.append('"%s"'%stockcode)
                values.append('"삼성전자"')
                values.append('"%s"'%stocks[1].text.replace(',', ''))
                values.append('"%s"'%stocks[-1].text.replace(',', ''))

                # db에 입력
                try: py2sql.insert(DB, 'main_stocks', stock_columns, ','.join(values))
                except: pass

url_form = 'https://finance.naver.com'
'/news/news_read.nhn?article_id=0012118752&office_id=001&mode=RANK&typ=0'

# Table Name : 'main_news'
def news(DB):
    print('뉴스 크롤링 시작')
    dtstr = '20210104'
    news_columns = 'date, title, content, publisher, url'
    BASE_URL = 'https://finance.naver.com/news/news_list.nhn?mode=RANK&date={}&page=1'
    r = requests.get(BASE_URL.format(dtstr))
    sp = BeautifulSoup(r.text, 'html.parser')

    news_list = sp.select('div.hotNewsList > ul.newsList ul.simpleNewsList li')
    for news in news_list:
        news_urls = news.select('a')
        values = []
        for news_url in news_urls:
            new_r = requests.get(url_form + news_url.attrs['href'])
            new_sp = BeautifulSoup(new_r.text, 'html.parser')
            body = new_sp.select_one('div.boardView')

            values.append('"%s"'%body.select_one('div.article_sponsor span.article_date').text)
            values.append('"%s"'%body.select_one('div.article_info h3').text.strip().replace('"', '<dq>')) # title
            values.append('"%s"'%body.select_one('div#content').text.strip().replace('"', '<dq>'))
            values.append('"%s"'%body.select_one('div.sponsor img').attrs['title']) #publisher
            values.append('"%s"'%body.select_one('div.article_sponsor a').attrs['href'])

            # db에 입력
            py2sql.insert(DB, 'main_news', news_columns, ','.join(values))
            # try: 
            # except: pass

if __name__ == "__main__":
    Scoin_DB = py2sql.conn()

    # stock(Scoin_DB)
    # news(Scoin_DB)
    coin(Scoin_DB)

