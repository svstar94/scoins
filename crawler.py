import requests
import json
from datetime import datetime
import pandas as pd

# 2021-01-04T13:00:00.000Z
dateformat = '%Y-%m-%dT%H:%M:%s.%fZ'

def coincrawl():
    dtnow = datetime.now()
    dt, ms = str(dtnow).split('.')
    dtstr = '.'.join([dt, ms[:3]])
    dtstr = dtstr.replace(' ', 'T') + 'Z'
    BASE_URL = 'https://crix-api-cdn.upbit.com/v1/crix/candles/days?code=CRIX.UPBIT.KRW-BTC&count=400&to={}'
    r = requests.get(BASE_URL.format(dtstr))

    res = json.loads(r.text)

    pd.DataFrame(res).to_csv('temp.csv')

if __name__ == "__main__":
    coincrawl()

