import statistics


class Helper:
    @staticmethod
    def gen_text(direction, trade_action):
        result = ''
        if direction == '买' and (trade_action == '开' or trade_action == '开仓'):
            result = 'B>'
        elif direction == '买' and (trade_action == '平' or trade_action == '平今'):
            result = '<B '  # + pnl_str
        elif direction == '卖' and (trade_action == '开' or trade_action == '开仓'):
            result = 'S>'
        elif direction == '卖' and (trade_action == '平' or trade_action == '平今'):
            result = '<S '  # + pnl_str
        else:
            print("Can't process data.")
        return result

    @staticmethod
    def convert_time_field(time_field):
        result = []
        time_field_tokens = time_field.split(':')
        minutes = int(int(time_field_tokens[1]) / 15)
        # if minutes < 3:
        #     minutes += 1
        formatted_15minute = '{:0>2d}'.format(minutes * 15)
        result.append(time_field_tokens[0] + formatted_15minute)
        return result

    @staticmethod
    def gen_color(trade_direction):
        if trade_direction == '买':
            return 'COLORRED'
        else:
            return 'COLORGREEN'

    @staticmethod
    def gen_align(trade_action):
        if trade_action == '开' or trade_action == '开仓':
            return 'ALIGN2,VALIGN1'
        else:
            return 'ALIGN0,VALIGN1'

    @staticmethod
    def generate_result(processor, line_tokens):
        result = []
        date_str = processor.get_date_str(line_tokens)
        time_str = processor.get_time_str(line_tokens)
        symbol_str = processor.get_symbol_str(line_tokens)
        direction_str = processor.get_direction_str(line_tokens)
        action_str = processor.get_action_str(line_tokens)
        text_str = Helper.gen_text(direction_str, action_str)
        price_str = processor.get_price_str(line_tokens)
        # DRAWTEXT(DATE=230512&&TIME=0900&&ISCONTRACT('OI309'),7956,'S>'),VALIGN1,COLORGREEN;
        for time_field in Helper.convert_time_field(time_str):
            result_str1 = 'DRAWTEXT(DATE=' + date_str + '&&TIME=' + time_field + '&&ISCONTRACT(\'' + symbol_str + '\'),' + price_str + ',\'' + text_str + '\'),' + Helper.gen_align(
                action_str) + ',' + Helper.gen_color(direction_str) + ';'
            print(result_str1)
            result.append(result_str1)
        return result
