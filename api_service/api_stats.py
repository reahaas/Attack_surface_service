import datetime

from consts import SECONDS_IN_DAY, MICROSECONDS_IN_SECOND


def add_to_average(average: float, size: int, value: float):
    """
    Thanks to: https://stackoverflow.com/a/22999488/8808983
    :param average:
    :param size:
    :param value:
    :return:
    """
    return (size * average + value) / (size + 1)


def convert_timedelta_to_microseconds(td: datetime.timedelta):
    delta_in_microseconds = td.microseconds + (td.seconds + td.days * SECONDS_IN_DAY) * MICROSECONDS_IN_SECOND
    return delta_in_microseconds


def convert_microseconds_to_float_seconds(delta_in_microseconds: float):
    return delta_in_microseconds / MICROSECONDS_IN_SECOND


class ApiStats:
    counter = 0
    average_request_time = 0
    
    @staticmethod
    def get_stats_data():
        stats = {
            "count": ApiStats.counter,
            "average_request_time": convert_microseconds_to_float_seconds(ApiStats.average_request_time)
        }
        return stats
    
    @staticmethod
    def increase_counter():
        ApiStats.counter += 1
        
    @staticmethod
    def update_averga_request_time(request_time: datetime.timedelta):
        request_time_in_microseconds = convert_timedelta_to_microseconds(request_time)
        ApiStats.average_request_time = add_to_average(ApiStats.average_request_time,
                                                       ApiStats.counter,
                                                       request_time_in_microseconds)
