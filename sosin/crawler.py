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
def coin(DB, code_id, coincode=None):
    print('코인 크롤링 시작')
    coin_columns = 'date, code_id, sise, amount'
    # 일별 비트코인 데이터
    BASE_URL = 'https://api.bithumb.com/public/candlestick_trview/{}_KRW/24H'
    r = requests.get(BASE_URL.format(coincode))
    try:
        res = json.loads(r.text)['data']
    except:
        return
    # 'c' = 종가
    # 't' = 기준 시간
    # 'v' = 거래량 (코인 개수 기준)

    for i in range(len(res['t'])):
        values = []
        t = time.gmtime(int(res['t'][i])/1000)

        values.append('"%s-%s-%s"'%(t.tm_year, t.tm_mon, t.tm_mday))
        values.append('"%s"'%code_id)
        values.append('"%s"'%res['c'][i])
        values.append('"%.2f"'%float(res['v'][i]))

        # db에 입력
        try: py2sql.insert(DB, 'homeapp_coin', coin_columns, ','.join(values))
        except: 
            print('코인 DB 입력 오류')
            pass

    # pd.DataFrame(res).to_csv('temp.csv')

def coin_test(code_id, coincode=None):
    DB = py2sql.conn()
    print('코인 크롤링 시작')
    coin_columns = 'date, code_id, sise, amount'
    # 일별 비트코인 데이터
    BASE_URL = 'https://api.bithumb.com/public/candlestick_trview/{}_KRW/24H'
    r = requests.get(BASE_URL.format(coincode))
    try:
        res = json.loads(r.text)['data']
    except:
        print( '코인 데이터 가져오기 오류' )
        return 'no data'
    # 'c' = 종가
    # 't' = 기준 시간
    # 'v' = 거래량 (코인 개수 기준)

    for i in range(len(res['t'])):
        values = []
        t = time.gmtime(int(res['t'][i])/1000)

        values.append('"%s-%s-%s"'%(t.tm_year, t.tm_mon, t.tm_mday))
        values.append('"%s"'%code_id)
        values.append('"%s"'%res['c'][i])
        values.append('"%.2f"'%float(res['v'][i]))

        # db에 입력
        try: py2sql.insert(DB, 'homeapp_coin', coin_columns, ','.join(values))
        except: 
            print('코인 DB 입력 오류')
            pass
    
    return 'finish'
    # pd.DataFrame(res).to_csv('temp.csv')

def get_coin_info(DB):
    COIN_URL = "https://api.upbit.com/v1/market/all"
    r = requests.get(COIN_URL)
    results = json.loads(r.text)
    for result in results:
        values = []
        if 'KRW' in result['market']:
            values.append('"%s"'%result['market'].split('-')[-1]) # code
            values.append('"%s"'%result['korean_name']) # name
            try:
                py2sql.insert(DB, 'homeapp_coininfo', 'code, name', ','.join(values))
            except:
                pass
            
import time

# Table Name : 'homeapp_stock'
def stock(DB, stockcode=None): # stock code는 stockinfo의 id값
    print('주식 크롤링 시작')
    stock_columns = 'date, code, sise, amount'
    BASE_URL = 'https://finance.naver.com/item/sise_day.nhn?code={}&page={}'

    for i in range(1, 30):
        time.sleep(1)
        print('%s page 크롤링 중...'%i)
        r = requests.get(BASE_URL.format(stockcode, i))
        sp = BeautifulSoup(r.text, 'html.parser')
        results = sp.select('tr')
        if len(results) == 0:
            print('주식 데이터 가져오기 오류')
            return
        for i, result in enumerate(results):
            if i in [2,3,4,5,6,10,11,12,13,14]:
                stocks = result.select('td')
                values = []
                # yyyy-mm-dd hh:mm:ss
                values.append('"%s"'%stocks[0].text.replace('.', '-'))
                values.append('"%s"'%stockcode)
                values.append('"%s"'%stocks[1].text.replace(',', ''))
                values.append('"%s"'%stocks[-1].text.replace(',', ''))

                # db에 입력
                try:
                    py2sql.insert(DB, 'homeapp_stock', stock_columns, ','.join(values))
                except: 
                    print('주식 DB 입력 오류')
                    pass

def stock_test(code_id, stockcode=None):
    DB = py2sql.conn()
    print('주식 크롤링 시작')
    stock_columns = 'date, code_id, sise, amount'
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    BASE_URL = 'https://finance.naver.com/item/sise_day.nhn?code={}&page={}'

    for i in range(1, 30):
        time.sleep(1)
        print('%s page 크롤링 중...'%i)
        r = requests.get(BASE_URL.format(stockcode, i), headers=header)
        sp = BeautifulSoup(r.text, 'html.parser')
        results = sp.select('tr')
        if len(results) == 0:
            print('크롤링이 안되는거')
            return
        for i, result in enumerate(results):
            if i in [2,3,4,5,6,10,11,12,13,14]:
                stocks = result.select('td')
                values = []
                # yyyy-mm-dd hh:mm:ss
                values.append('"%s"'%stocks[0].text.replace('.', '-'))
                values.append('"%s"'%code_id)
                values.append('"%s"'%stocks[1].text.replace(',', ''))
                values.append('"%s"'%stocks[-1].text.replace(',', ''))

                # db에 입력
                try:
                    py2sql.insert(DB, 'homeapp_stock', stock_columns, ','.join(values))
                except: pass

url_form = 'https://finance.naver.com'
'/news/news_read.nhn?article_id=0012118752&office_id=001&mode=RANK&typ=0'

# Table Name : 'main_news'
def news(DB):
    print('뉴스 크롤링 시작')
    dtstr = datetime.now().date().strftime('%Y%m%d')
    news_columns = 'date, title, content, publisher, url'
    page=1
    sample_news = None
    while True:
        BASE_URL = 'https://finance.naver.com/news/news_list.nhn?mode=RANK&date={}&page={}'
        r = requests.get(BASE_URL.format(dtstr, page))
        sp = BeautifulSoup(r.text, 'html.parser')
        news_list = sp.select('div.hotNewsList > ul.newsList ul.simpleNewsList li')
        if sample_news == news_list:
            break
        
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
                py2sql.insert(DB, 'homeapp_news', news_columns, ','.join(values))
                # try: 
                # except: pass

        page += 1
        sample_news = news_list

def get_stock_info(DB):
    print('주식 정보 가져오기')
    dfstockcode = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
    for row in dfstockcode.iloc:
        code = '"%06d"'%row['종목코드']
        name = '"%s"'%row['회사명']
        py2sql.insert(DB, 'homeapp_stockinfo', 'code, name' ,f'{code},{name}')

if __name__ == "__main__":
    Scoin_DB = py2sql.conn()

    # stock(Scoin_DB)
    news(Scoin_DB)

    # 코인 Code Crawling
    get_coin_info(Scoin_DB)

    # 코인 코드 가져오기
    db_result = py2sql.select(Scoin_DB, 'homeapp_coininfo', '*')
    print(db_result[2])

    # 코인 데이터 크롤링
    for code_id, code, _ in db_result:
        coin_test(code_id, code)

    # 주식 code crawling
    get_stock_info(Scoin_DB)

    # 주식 코드 가져오기
    db_result = py2sql.select(Scoin_DB, 'homeapp_stockinfo', '*')
    print(db_result[0])
    # for stock_id, code, _ in db_result:
    #     stock_test(stock_id, code)
    
    Scoin_DB.close()