import time
from functools import wraps
from datetime import datetime, timedelta


def timer(function):
    @wraps(function)
    def wrapper(*args, **kargs):
        start_time = time.time()
        result = function(*args, **kargs)
        print("Runtime of {0}: {1}s".format(function.__name__, time.time()-start_time))
        return result
    return wrapper


def get_local_time(date, GMT):
    start_time = datetime.strptime('{0}T00:00:00'.format(date), '%Y-%m-%dT%H:%M:%S')
    end_time = datetime.strptime('{0}T23:59:59'.format(date), '%Y-%m-%dT%H:%M:%S')
    start_time_sd = (start_time - timedelta(hours=GMT)).strftime('%Y-%m-%dT%H:%M:%S')
    end_time_sd = (end_time - timedelta(hours=GMT)).strftime('%Y-%m-%dT%H:%M:%S')
    return start_time_sd, end_time_sd


def get_dates(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    date_range = int((end_date - start_date) / timedelta(days=1)) + 1  # include last day
    return [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(date_range)]


def get_HK_stock_symbols():
    from bs4 import BeautifulSoup
    import requests
    page_link = 'http://eoddata.com/stocklist/HKEX.htm'
    page_response = requests.get(page_link, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    symobl_table = page_content.find('table', class_='quotes')
    syms = []
    for row in symobl_table.find_all('tr', class_=['ro', 're']):
        syms.append(row.find('a').text[1:] + '.HK')
    return syms