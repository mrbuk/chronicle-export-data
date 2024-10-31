import unittest
from datetime import datetime, timedelta
from date_calculator import DateCalculator

class TestDateCalculator(unittest.TestCase):

    def test_270d_in_past(self):
        date = datetime(2024,10,30)
        calculator = DateCalculator(date)
        ranges = calculator.ranges

        self.assertEqual(len(ranges), 4)

        start_time = ranges[0][0]
        end_time = ranges[0][1]
        self.assertEqual(start_time.hour, 0)
        self.assertEqual(start_time.minute, 0)
        self.assertEqual(start_time.second, 0)
        self.assertEqual(start_time.day, 3)
        self.assertEqual(start_time.month, 2)
        self.assertEqual(start_time.year, 2024)

        self.assertEqual(end_time.hour, 6)
        self.assertEqual(end_time.minute, 0)
        self.assertEqual(end_time.second, 0)
        self.assertEqual(end_time.day, 3)
        self.assertEqual(end_time.month, 2)
        self.assertEqual(end_time.year, 2024)

        start_time = ranges[1][0]
        end_time = ranges[1][1]
        self.assertEqual(start_time.hour, 6)
        self.assertEqual(start_time.minute, 0)
        self.assertEqual(start_time.second, 0)
        self.assertEqual(start_time.day, 3)
        self.assertEqual(start_time.month, 2)
        self.assertEqual(start_time.year, 2024)

        self.assertEqual(end_time.hour, 12)
        self.assertEqual(end_time.minute, 0)
        self.assertEqual(end_time.second, 0)
        self.assertEqual(end_time.day, 3)
        self.assertEqual(end_time.month, 2)
        self.assertEqual(end_time.year, 2024)

        start_time = ranges[2][0]
        end_time = ranges[2][1]
        self.assertEqual(start_time.hour, 12)
        self.assertEqual(start_time.minute, 0)
        self.assertEqual(start_time.second, 0)
        self.assertEqual(start_time.day, 3)
        self.assertEqual(start_time.month, 2)
        self.assertEqual(start_time.year, 2024)

        self.assertEqual(end_time.hour, 18)
        self.assertEqual(end_time.minute, 0)
        self.assertEqual(end_time.second, 0)
        self.assertEqual(end_time.day, 3)
        self.assertEqual(end_time.month, 2)
        self.assertEqual(end_time.year, 2024)

        start_time = ranges[3][0]
        end_time = ranges[3][1]
        self.assertEqual(start_time.hour, 18)
        self.assertEqual(start_time.minute, 0)
        self.assertEqual(start_time.second, 0)
        self.assertEqual(start_time.day, 3)
        self.assertEqual(start_time.month, 2)
        self.assertEqual(start_time.year, 2024)

        self.assertEqual(end_time.hour, 0)
        self.assertEqual(end_time.minute, 0)
        self.assertEqual(end_time.second, 0)
        self.assertEqual(end_time.day, 4)
        self.assertEqual(end_time.month, 2)
        self.assertEqual(end_time.year, 2024)

if __name__ == '__main__':
    unittest.main()
