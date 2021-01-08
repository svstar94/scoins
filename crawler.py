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
        try: py2sql.insert(DB, 'homeapp_coin', coin_columns, ','.join(values))
        
        except: pass
        'homeapp_coininfo'

    # pd.DataFrame(res).to_csv('temp.csv')


import time

# Table Name : 'homeapp_stock'
def stock(DB, stockcode=None):
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
    dfstockcode = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
    for row in dfstockcode.iloc:
        code = '"%06d"'%row['종목코드']
        name = '"%s"'%row['회사명']
        py2sql.insert(DB, 'homeapp_stockinfo', 'code, name' ,f'{code},{name}')

from selenium import webdriver
def get_coin_info(DB):
    pass

if __name__ == "__main__":
    Scoin_DB = py2sql.conn()

    # stock(Scoin_DB)
    # news(Scoin_DB)
    # coin(Scoin_DB)

    # 주식 code crawling
    # get_stock_info(Scoin_DB)

    # 주식 코드 가져오기
    db_result = py2sql.select(Scoin_DB, 'homeapp_stockinfo', '*')
    print(db_result[0])

    # 주식 시세 크롤링
    driver = webdriver.Chrome(r'D:\INSTA\insta_tistory\webdriver\chromedriver.exe')
    stock_columns = 'date, code_id, sise, amount'
    # Tuple -> column values
    for code_id, code, name in db_result:
        if code_id < 3:
            continue
        for p in range(1, 30):
            driver.get('https://finance.naver.com/item/sise_day.nhn?code={}&page={}'.format(code, p))
            results = driver.find_elements_by_css_selector('tr')
            try:
                if datetime.strptime(results[5].find_element_by_css_selector('td').text, '%Y.%m.%d') < datetime(2018,1,1):
                    time.sleep(1)
                    break
            except:
                break

            for i, result in enumerate(results):
                if i in [2,3,4,5,6,10,11,12,13,14]:
                    stocks = result.find_elements_by_css_selector('td')

                    values = []
                    # yyyy-mm-dd hh:mm:ss
                    values.append('"%s"'%stocks[0].text.replace('.', '-'))
                    values.append('"%s"'%code_id)
                    values.append('"%s"'%stocks[1].text.replace(',', ''))
                    values.append('"%s"'%stocks[-1].text.replace(',', ''))
                    if values[0] == '""':
                        continue

                    # db에 입력
                    # try:
                    py2sql.insert(Scoin_DB, 'homeapp_stock', stock_columns, ','.join(values))
                    # except: pass
            time.sleep(1)
