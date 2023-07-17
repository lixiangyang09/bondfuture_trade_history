from input import input_processor
import os
from cfets_calendar.calendar import CfetsCalendar
import datetime
import time
import shutil
from common.logger import logger


class KuaiQi(input_processor.InputProcessor):

    # 获取文件对应的交易日期，并对文件进行备份
    def __init__(self, file_path, file_name):
        file_full_path = os.path.join(file_path, file_name)
        file_modified_time = os.path.getmtime(file_full_path)
        file_modified_local_time = time.localtime(file_modified_time)
        self.clear_file_full_path = None
        # 交易记录文件小于当晚的21点，则认为交易是当日的，则需要对文件进行备份，以防止夜盘的文件覆盖了白天的交易记录
        if file_modified_local_time.tm_hour < 21 and "backup" not in file_name:
            backup_file_full_path = os.path.join(file_path, file_name + "backup")
            shutil.copy2(file_full_path, backup_file_full_path)
            self.clear_file_full_path = file_full_path
            logger.info("backup file: %s", self.clear_file_full_path)

        self.tokens = None
        self.file_modified_local_time = file_modified_local_time
        self.file_name = file_name
        self.calendar = CfetsCalendar()
        # 分析之后的当前交易文件应该归属的交易日期
        self.trade_date = self.get_trade_date()

    def clear_file(self):
        if self.clear_file_full_path:
            os.remove(self.clear_file_full_path)
            logger.info("Remove file: %s", self.clear_file_full_path)

    def get_trade_date(self):
        name_tokens = self.file_name.split('.')
        # 230714
        trade_date = name_tokens[0].split('_')[1]
        trade_datetime_origin = datetime.datetime(self.file_modified_local_time.tm_year, int(trade_date[2:4]), int(trade_date[4:6]))
        final_trade_day = None
        # 如果当天是交易日，且文件修改时间为21点之前的，则交易记录为当天
        # 如果当天为节假日，或者当天为交易日但是文件的修改时间为21点之后，则调整到下一个交易日
        if self.calendar.is_trading_day(trade_datetime_origin) and self.file_modified_local_time.tm_hour < 21:
            final_trade_day = trade_datetime_origin
        else:
            if (not self.calendar.is_trading_day(trade_datetime_origin)) or (self.calendar.is_trading_day(trade_datetime_origin) and self.file_modified_local_time.tm_hour >= 21):
                final_trade_day = self.calendar.next_trading_day(trade_datetime_origin)
        return final_trade_day

    def get_date_str(self, tokens):
        return self.trade_date.strftime("%Y%m%d")[2:8]

    def get_time_str(self, tokens):
        return tokens[6]

    def get_symbol_str(self, tokens):
        return tokens[1]

    def get_direction_str(self, tokens):
        return tokens[2]

    def get_action_str(self, tokens):
        return tokens[3]

    def get_price_str(self, tokens):
        return tokens[4]

