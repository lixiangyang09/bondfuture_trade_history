# This is a sample Python script.
import os
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import shutil
import datetime

# 原始文件中的数据，以防止当天多次导出，记录重复
whole_data_lines = set()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def gen_text(direction, trade_action, pnl_str):
    result = ''
    if direction == '买' and trade_action == '开':
        result = 'B>'
    elif direction == '买' and (trade_action == '平' or trade_action == '平今'):
        result = '<B ' # + pnl_str
    elif direction == '卖' and trade_action == '开':
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
    if trade_action == '开':
        return 'ALIGN2,VALIGN1'
    else:
        return 'ALIGN0,VALIGN1'


# 目前只生成了15分钟的数据
def gen_result(line_tokens):
    result = []
    date_str = line_tokens[0]
    instrument_str = line_tokens[3]
    text_str = gen_text(line_tokens[4], line_tokens[5], line_tokens[8])
    price_str = line_tokens[6]
    # DRAWTEXT(DATE=230512&&TIME=0900&&ISCONTRACT('OI309'),7956,'S>'),VALIGN1,COLORGREEN;
    for time_field in convert_time_field(line_tokens[1]):
        result_str1 = 'DRAWTEXT(DATE=' + date_str[2:] + '&&TIME=' + time_field + '&&ISCONTRACT(\'' + instrument_str + '\'),' + price_str + ',\'' + text_str + '\'),' + gen_align(line_tokens[5]) + ',' + gen_color(line_tokens[4]) + ';'
        print(result_str1)
        if result_str1 not in whole_data_lines:
            result.append(result_str1)
            whole_data_lines.add(result_str1)
    return result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    source_data_dir = "data"
    target_file_origin = "D:\wh6通用版\Formula\TYPES\自编\TRADE_HISTORY_15M.XTRD"
    target_file_backup = "target_backup"
    shutil.copyfile(target_file_origin, target_file_backup)

    origin_lines = set()
    result_lines = set()

    # 读取当前已有的记录，后续去重用
    with open(target_file_origin, 'r', encoding='GB18030') as target_file_origin_handler:
        for line in target_file_origin_handler.readlines():
            line_stripped = line.strip()
            if line_stripped == '</CODE>':
                break
            if line_stripped and 'CODE' not in line_stripped:
                origin_lines.add(line_stripped)

    # 读取数据文件夹下的交易记录
    for data_file in os.listdir(source_data_dir):
        print(data_file)
        if data_file.startswith("."):
            print("Skipe file", data_file)
            continue
        with open(os.path.join(source_data_dir, data_file), 'r', encoding='GB18030') as file_input:
            file_lines = file_input.readlines()
            for file_line in file_lines:
                print(file_line)
                tokens = re.split(' |,', file_line)
                # tokens = file_line.split(" ")
                filtered_tokens = []
                for token in tokens:
                    if token:
                        # print(token.strip())
                        filtered_tokens.append(token.strip())
                print(tokens)
                # 最后一行
                if "20" not in filtered_tokens[0]:
                    continue
                if ":" not in filtered_tokens[1]:
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
