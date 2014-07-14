import string
import random
import calendar

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def generate_random_string(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def get_unix_timestamp(datetime_val):
        return calendar.timegm(datetime_val.utctimetuple())
