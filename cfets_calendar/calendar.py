import requests
from lxml import etree
import os
import time
import json
import datetime
from common.logger import logger


local_cache_file = 'local_cache/response_from_cfets_calendar'
now_time = time.localtime(time.time())
calendar_set = set()


def from_cached_file():
    with open(local_cache_file, encoding='utf-8') as input_file:
        line = input_file.readline()
        data = json.loads(line)
        calendar_list = data['data']['currencyCN'][str(now_time.tm_year)]
        for calendar_single in calendar_list:
            month = int(calendar_single[0:2])
            day = int(calendar_single[3:5])
            calendar_set.add(datetime.datetime(now_time.tm_year, month, day))


def from_cfets():
    logger.info("Request calendar from cfest.")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    url = 'https://www.chinamoney.com.cn/ags/ms/cm-s-holiday/depRMBTradingCal'
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        with open(local_cache_file, 'w', encoding='utf-8') as output_file:
            output_file.write(res.text)
        return True
    else:
        logger.warn("Request cfets calendar failed, will use the cache")
        return False


def load_calendar():
    # 每天只用请求1次
    if os.path.exists(local_cache_file):
        file_modified_time = os.path.getmtime(local_cache_file)
        print(file_modified_time)
        file_local_time = time.localtime(file_modified_time)
        if now_time.tm_year == file_local_time.tm_year and \
                now_time.tm_mon == file_local_time.tm_mon and \
                now_time.tm_mday == file_local_time.tm_mday:
            pass
        else:
            from_cfets()
    else:
        from_cfets()

    from_cached_file()
    logger.info("Loaded calendar is %s", calendar_set)
