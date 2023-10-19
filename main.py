# This is a sample Python script.
import cfets_calendar
import os
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import shutil
import datetime

# 原始文件中的数据，以防止当天多次导出，记录重复
from common.file_type import FileType
from input.kuaiqi import KuaiQi
from input.wenhua import WenHua
from common.logger import logger
from common.helper import Helper
from common.settings import Settings

# 数据目录
data_folder_path = 'C:\\work\\bondfuture_trade_history\\data'

target_file_list = ["C:\wh6通用版\Formula\TYPES\自编\TRADE_HISTORY_15M.XTRD",
                    "C:\wh6通用版\Formula\TYPES\自编\TRADE_HISTORY_5M.XTRD",]
target_time_precision_list = [15, 5]
# data_folder_path = 'data'
# target_file = "15M.XTRD"
target_file_backup = "target_backup"

# 生成的最终数据集
final_result_set = set()


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
    # shutil.copyfile(target_file, target_file_backup)

    # 读取当前已有的记录，后续去重用
    # origin_lines = set()
    # with open(target_file, 'r', encoding='GB18030') as target_file_origin_handler:
    #     for line in target_file_origin_handler.readlines():
    #         line_stripped = line.strip()
    #         if line_stripped == '</CODE>':
    #             break
    #         if line_stripped and 'CODE' not in line_stripped:
    #             origin_lines.add(line_stripped)
    # 原有的数据，也需要进行保留
    # final_result_set.update(origin_lines)
    # 读取数据文件夹下的交易记录
    candidate_files = os.listdir(data_folder_path)
    candidate_files.sort(reverse=False)
    total_count = 0
    for data_file in candidate_files:
        if total_count > 2500:
            print(f'skip {data_file} due to count')
        deduplicate = set()
        filtered_lines = []
        file_type = identify_file_type(data_file)
        file_full_path = os.path.join(data_folder_path, data_file)

        if file_type == FileType.WEN_HUA:
            file_processor = WenHua()
        elif file_type == FileType.KUAI_QI:
            file_processor = KuaiQi(data_folder_path, data_file)
        else:
            logger.warn("Ignore file:%s", file_full_path)
            continue
        with open(file_full_path, 'r', encoding='GB18030') as file_input:
            file_lines = file_input.readlines()
            for file_line in file_lines:
                file_line = file_line.strip()
                tokens = re.split(' |,', file_line)
                # tokens = file_line.split(" ")
                filtered_tokens = []
                for token in tokens:
                    if token.strip():
                        filtered_tokens.append(token.strip())
                # print(filtered_tokens)
                # 过滤空行
                if not filtered_tokens:
                    continue
                if ":" not in file_processor.get_time_str(filtered_tokens):
                    continue
                if file_line not in deduplicate:
                    filtered_lines.append(filtered_tokens)
                deduplicate.add(file_line)
        print(file_full_path)
        total_count += len(filtered_lines)
        for filtered_line in filtered_lines:
            line_result = Helper.generate_result(file_processor, filtered_line)
            final_result_set.update(line_result)
        file_processor.clear_file()


def generate_result_file(target_file):
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
    for index in range(0, len(target_file_list)):
        target_file = target_file_list[index]
        target_precison = target_time_precision_list[index]
        logger.info(f"process {target_file} with {target_precison}")
        Settings.set_time_precision(target_precison)
        Settings.set_target_file_name(target_file)
        final_result_set.clear()
        # 加载数据目录
        process_data_folder()

        # 生成最终结果
        generate_result_file(target_file)


