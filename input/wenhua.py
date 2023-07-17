from input import input_processor


class WenHua(input_processor.InputProcessor):

    def get_date_str(self, tokens):
        return tokens[0][2:]

    def get_time_str(self, tokens):
        return tokens[1]

    def get_symbol_str(self, tokens):
        return tokens[3]

    def get_direction_str(self,tokens):
        return tokens[4]

    def get_action_str(self, tokens):
        return tokens[5]

    def get_price_str(self, tokens):
        return tokens[6]

