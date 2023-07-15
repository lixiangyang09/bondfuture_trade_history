# This is a sample Python script.
import cfets_calendar
import os
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import shutil
import datetime

# 原始文件中的数据，以防止当天多次导出，记录重复
from cfets_calendar.calendar import load_calendar, calendar_set
from common.file_type import FileType
from input import wenhua,kuaiqi
from common.logger import logger

# 数据目录
data_folder_path = 'data'
target_file = "D:\wh6通用版\Formula\TYPES\自编\TRADE_HISTORY_15M.XTRD"
target_file_backup = "target_backup"

# 生成的最终数据集
final_result_set = set()


#文华(0)，或者快期(1)
software_kind = 0
trade_date_index=[0,]
trade_time_index=[1,6]
symbol_index=[3,1]
direction_index=[4,2]
trade_action_index=[5,3]
price_index=[6,4]

kuaiqi_trade_date=''


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def gen_text(direction, trade_action):
    result = ''
    if direction == '买' and (trade_action == '开' or trade_action == '开仓'):
        result = 'B>'
    elif direction == '买' and (trade_action == '平' or trade_action == '平今'):
        result = '<B ' # + pnl_str
    elif direction == '卖' and (trade_action == '开' or trade_action == '开仓'):
        result = 'S>'
    elif direction == '卖' and (trade_action == '平' or trade_action == '平今'):
        result = '<S ' # + pnl_str
    else:
        print("Can't process data.")
    return result


def convert_time_field(time_field):
    result = []
    time_field_tokens = time_field.split(':')
    minutes = int(int(time_field_tokens[1]) / 15)
    # if minutes < 3:
    #     minutes += 1
    formatted_15minute = '{:0>2d}'.format(minutes * 15)
    result.append(time_field_tokens[0] + formatted_15minute)
    return result


def gen_color(trade_direction):
    if trade_direction == '买':
        return 'COLORRED'
    else:
        return 'COLORGREEN'


def gen_align(trade_action):
    if trade_action == '开' or trade_action == '开仓':
        return 'ALIGN2,VALIGN1'
    else:
        return 'ALIGN0,VALIGN1'


def get_date_str(line_tokens):
    if software_kind == 1:
        return kuaiqi_trade_date
    elif software_kind == 0:
        return line_tokens[trade_date_index[0]][2:]


def get_symbol_str(line_tokens):
    return line_tokens[symbol_index[software_kind]]


def get_direction_str(line_tokens):
    return line_tokens[direction_index[software_kind]]


def get_action_str(line_tokens):
    return line_tokens[trade_action_index[software_kind]]


def get_price_str(line_tokens):
    return line_tokens[price_index[software_kind]]


def get_time_str(line_tokens):
    return line_tokens[trade_time_index[software_kind]]


# 目前只生成了15分钟的数据
def gen_result(line_tokens):
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
        result_str1 = 'DRAWTEXT(DATE=' + date_str + '&&TIME=' + time_field + '&&ISCONTRACT(\'' + symbol_str + '\'),' + price_str + ',\'' + text_str + '\'),' + gen_align(action_str) + ',' + gen_color(direction_str) + ';'
        print(result_str1)
        if result_str1 not in whole_data_lines:
            result.append(result_str1)
            whole_data_lines.add(result_str1)
    return result


def process():

    origin_lines = set()
    result_lines = set()



    # 读取数据文件夹下的交易记录
    for data_file in os.listdir(source_data_dir):
        print(data_file)
        software_kind = 0
        if data_file.startswith("."):
            print("Skipe file", data_file)
            continue
        if '成交记录' in data_file:
            name_tokens = data_file.split('.')
            kuaiqi_trade_date=name_tokens[0].split('_')[1]
            software_kind = 1
        with open(os.path.join(source_data_dir, data_file), 'r', encoding='GB18030') as file_input:
            file_lines = file_input.readlines()
            for file_line in file_lines:
                print(file_line)
                file_line = file_line.strip()
                tokens = re.split(' |,', file_line)
                # tokens = file_line.split(" ")
                filtered_tokens = []
                for token in tokens:
                    if token:
                        # print(token.strip())
                        filtered_tokens.append(token.strip())
                print(filtered_tokens)
                # 过滤空行
                if not filtered_tokens:
                    continue
                if ":" not in filtered_tokens[trade_time_index[software_kind]]:
                    continue
                line_results = gen_result(filtered_tokens)
                for line_result in line_results:
                    result_lines.add(line_result)

    # 删除文件
    os.remove(target_file_origin)

    # 合并结果
    final_result = []
    for line in origin_lines:
        final_result.append(line)
    for line in result_lines:
        if line not in origin_lines:
            final_result.append(line)
    final_result.sort(reverse=True)
    # 生成新的目标文件
    with open(target_file_origin, 'w', encoding='GB18030') as target_file_handler:
        target_file_handler.write('<CODE>\n')
        for line in final_result:
            target_file_handler.write(line + '\n')

        target_file_handler.write('</CODE>\n')
        target_file_handler.write('<VERSION>\n')
        target_file_handler.write('130112\n')
        target_file_handler.write('</VERSION>\n')
        target_file_handler.write('<EDITTIME>\n')

        target_file_handler.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
        target_file_handler.write('</EDITTIME>\n')
        target_file_handler.write('<PROPERTY>\n')
        target_file_handler.write('1\n')
        target_file_handler.write('</PROPERTY>\n')
        target_file_handler.write('\n')


# 根据文件名识别软件类型
def identify_file_type(file_name):
    if '成交记录' in file_name:
        return FileType.KUAI_QI
    elif 'txt' in file_name:
        return FileType.WEN_HUA
    else:
        return None


def process_data_folder():
    # 备份目标文件
    shutil.copyfile(target_file, target_file_backup)

    # 读取当前已有的记录，后续去重用
    origin_lines = set()
    with open(target_file, 'r', encoding='GB18030') as target_file_origin_handler:
        for line in target_file_origin_handler.readlines():
            line_stripped = line.strip()
            if line_stripped == '</CODE>':
                break
            if line_stripped and 'CODE' not in line_stripped:
                origin_lines.add(line_stripped)
    # 原有的数据，也需要进行保留
    final_result_lines.update(line_stripped)
    # 读取数据文件夹下的交易记录
    for data_file in os.listdir(data_folder_path):
        file_type = identify_file_type(data_file)
        file_full_path = os.path.join(data_folder_path, data_file)

        if file_type == FileType.WEN_HUA:
            final_result_lines.update(wenhua.process(file_full_path))
        elif file_type == FileType.KUAI_QI:
            final_result_lines.update(kuaiqi.process(file_full_path))
        else:
            logger.warn("Ignore file:%s", file_full_path)


def generate_result_file():
    os.remove(target_file)
    # 合并结果
    final_result = []
    for line in final_result_set:
        final_result.append(line)
    final_result.sort(reverse=True)
    # 生成新的目标文件
    with open(target_file, 'w', encoding='GB18030') as target_file_handler:
        target_file_handler.write('<CODE>\n')
        for line in final_result:
            target_file_handler.write(line + '\n')

        target_file_handler.write('</CODE>\n')
        target_file_handler.write('<VERSION>\n')
        target_file_handler.write('130112\n')
        target_file_handler.write('</VERSION>\n')
        target_file_handler.write('<EDITTIME>\n')

        target_file_handler.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
        target_file_handler.write('</EDITTIME>\n')
        target_file_handler.write('<PROPERTY>\n')
        target_file_handler.write('1\n')
        target_file_handler.write('</PROPERTY>\n')
        target_file_handler.write('\n')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # 加载交易日历
    load_calendar()
    print(calendar_set)

    # 加载数据目录
    process_data_folder()

    # 生成最终结果
    generate_result_file()


