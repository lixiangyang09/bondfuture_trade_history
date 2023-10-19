

class Settings:
    target_file_name = None
    time_precision = None

    @classmethod
    def set_target_file_name(cls,target_file_name):
        cls.target_file_name = target_file_name

    @classmethod
    def set_time_precision(cls, time_precision):
        cls.time_precision = time_precision

