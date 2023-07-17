import requests
from lxml import etree
import os
import time
import json
import datetime
from common.logger import logger


class CfetsCalendar:
    def __init__(self):
        self.local_cache_file = 'local_cache/response_from_cfets_calendar'
        self.now_time = time.localtime(time.time())
        self.calendar_set = set()
        self.load_calendar()

    def from_cached_file(self):
        with open(self.local_cache_file, encoding='utf-8') as input_file:
            line = input_file.readline()
            data = json.loads(line)
            calendar_list = data['data']['currencyCN'][str(self.now_time.tm_year)]
            for calendar_single in calendar_list:
                month = int(calendar_single[0:2])
                day = int(calendar_single[3:5])
                self.calendar_set.add(datetime.datetime(self.now_time.tm_year, month, day))

    def from_cfets(self):
        logger.info("Request calendar from cfest.")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        url = 'https://www.chinamoney.com.cn/ags/ms/cm-s-holiday/depRMBTradingCal'
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            with open(self.local_cache_file, 'w', encoding='utf-8') as output_file:
                output_file.write(res.text)
            return True
        else:
            logger.warn("Request cfets calendar failed, will use the cache")
            return False

    def load_calendar(self):
        # 每天只用请求1次
        if os.path.exists(self.local_cache_file):
            file_modified_time = os.path.getmtime(self.local_cache_file)
            file_local_time = time.localtime(file_modified_time)
            if self.now_time.tm_year == file_local_time.tm_year and \
                    self.now_time.tm_mon == file_local_time.tm_mon and \
                    self.now_time.tm_mday == file_local_time.tm_mday:
                pass
            else:
                self.from_cfets()
        else:
            self.from_cfets()

        self.from_cached_file()

    def is_trading_day(self, day):
        a = day.weekday()
        b = day not in self.calendar_set
        if 0 <= day.weekday() < 5 and day not in self.calendar_set:
            return True
        else:
            return False

    def next_trading_day(self, day):
        while True:
            day = day + datetime.timedelta(1)
            if self.is_trading_day(day):
                return day
