from datetime import datetime, timedelta

class DateCalculator:
    NO_OF_RANGES = 4
    DELTA_IN_DAYS = 9 * 30

    def __init__(self, date=None):
        if not date:
            self.date = datetime.now().replace(hour=0, minute=0, second=0)
        else:
            self.date = date.replace(hour=0, minute=0, second=0)

    @property
    def ranges(self):
        arr = []
        secs_in_day = 86400
        d = self.date - timedelta(days=self.DELTA_IN_DAYS)

        i = 0
        while i < self.NO_OF_RANGES:
            start_date = d + timedelta(seconds=i * (secs_in_day / self.NO_OF_RANGES))
            end_date = start_date + timedelta(seconds=secs_in_day / self.NO_OF_RANGES)
            arr.append((start_date, end_date))
            i = i + 1

        return arr
