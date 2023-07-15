from input_processor import InputProcessor
import os
from cfets_calendar.calendar import calendar_set
import datetime
import time
import shutil


class KuaiQi(InputProcessor):

    # 获取文件对应的交易日期，并对文件进行备份
    def __init__(self, file_path, file_name):
        file_full_path = os.path.join(file_path, file_name)
        file_modified_time = os.path.getmtime(file_full_path)
        file_modified_local_time = time.localtime(file_modified_time)
        # 交易记录文件小于当晚的21点，则认为交易是当日的，则需要对文件进行备份，以防止夜盘的文件覆盖了白天的交易记录
        if file_modified_local_time.tm_hour < 21:
            backup_file_full_path = os.path.join(file_path, file_name + "backup")
            shutil.copy(file_full_path, backup_file_full_path)

        self.tokens = None
        self.file_modified_local_time = file_modified_local_time
        self.file_name = file_name
        # 分析之后的当前交易文件应该归属的交易日期
        self.trade_date = self.get_trade_date()

    def get_trade_date(self):
        name_tokens = self.file_name.split('.')
        # 230714
        trade_date = name_tokens[0].split('_')[1]
        trade_datetime_origin = datetime.datetime(self.file_modified_local_time.tm_year, int(trade_date[2:4]), int(trade_date[4:6]))
        # 如果当天是交易日，且文件修改时间为21点之前的，则交易记录为当天
        # 如果当天为节假日，或者当天为交易日但是文件的修改时间为21点之后，则调整到下一个交易日
        if


    def get_date_str(line_tokens):
        return line_tokens[trade_date_index[0]][2:]


    def process_line(self, tokens):
        result = []
        date_str = get_date_str(line_tokens)
        time_str = get_time_str(line_tokens)
        symbol_str = get_symbol_str(line_tokens)
        direction_str = get_direction_str(line_tokens)
        action_str = get_action_str(line_tokens)
        text_str = gen_text(direction_str, action_str)
        price_str = get_price_str(line_tokens)
        # DRAWTEXT(DATE=230512&&TIME=0900&&ISCONTRACT('OI309'),7956,'S>'),VALIGN1,COLORGREEN;
        for time_field in convert_time_field(time_str):
            result_str1 = 'DRAWTEXT(DATE=' + date_str + '&&TIME=' + time_field + '&&ISCONTRACT(\'' + symbol_str + '\'),' + price_str + ',\'' + text_str + '\'),' + gen_align(
                action_str) + ',' + gen_color(direction_str) + ';'
            print(result_str1)
            if result_str1 not in whole_data_lines:
                result.append(result_str1)
                whole_data_lines.add(result_str1)
        return result
