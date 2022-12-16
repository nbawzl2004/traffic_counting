'''
This module contains unit tests for class TrafficCounter
'''

import unittest
from traffic_counter import TrafficCounter


class WidgetTestCase(unittest.TestCase):
    '''
    Test class for TrafficCounter
    '''

    def setUp(self):
        pass

    def test_empty(self):
        tc = TrafficCounter()
        self.assertEqual(tc.total_cars, 0)

    def test_simple(self):
        input_lines = [
            '2021-12-01T05:00:00 5',
            '2021-12-01T05:30:00 12',
            '2021-12-01T06:00:00 14',
        ]
        traffic_counter = TrafficCounter()
        for line in input_lines:
            traffic_counter.process_line(line)
        self.assertEqual(traffic_counter.total_cars, 31)
        self.assertDictEqual(traffic_counter.date_total, {'2021-12-01': 31})
        self.assertEqual(
            traffic_counter.get_least_count_one_and_half_hour_record(),
            '2021-12-01T05:00:00 31'
        )

    def test_contiguous_two_day(self):
        input_lines = [
            '2021-12-01T23:00:00 5',
            '2021-12-01T23:30:00 12',
            '2021-12-02T00:00:00 14',
            '2021-12-02T00:30:00 99',
        ]
        traffic_counter = TrafficCounter()
        for line in input_lines:
            traffic_counter.process_line(line)
        self.assertEqual(traffic_counter.total_cars, 130)
        self.assertDictEqual(traffic_counter.date_total, {
                             '2021-12-01': 17, '2021-12-02': 113})
        self.assertListEqual(
            traffic_counter.get_top_three_record(),
            [
                '2021-12-02T00:30:00 99',
                '2021-12-02T00:00:00 14',
                '2021-12-01T23:30:00 12',
            ]
        )

        self.assertEqual(
            traffic_counter.get_least_count_one_and_half_hour_record(),
            '2021-12-01T23:00:00 31'
        )

    def test_two_day_with_1_gap(self):
        input_lines = [
            '2021-12-01T23:00:00 1',
            # skip a half hour record: '2021-12-01T23:30:00'
            '2021-12-02T00:00:00 3',
            '2021-12-02T00:30:00 2',
            '2021-12-02T01:00:00 0',
        ]
        traffic_counter = TrafficCounter()
        for line in input_lines:
            traffic_counter.process_line(line)
        self.assertEqual(traffic_counter.total_cars, 6)
        self.assertDictEqual(traffic_counter.date_total, {
                             '2021-12-01': 1, '2021-12-02': 5})
        self.assertListEqual(
            traffic_counter.get_top_three_record(),
            [
                '2021-12-02T00:00:00 3',
                '2021-12-02T00:30:00 2',
                '2021-12-01T23:00:00 1',
            ]
        )

        self.assertEqual(
            traffic_counter.get_least_count_one_and_half_hour_record(),
            '2021-12-01T23:00:00 4'
        )

    def test_two_day_with_2_gap(self):
        input_lines = [
            '2021-12-01T23:00:00 2',
            # skip a half hour record:      '2021-12-01T23:30:00'
            # skip another half hour record:'2021-12-02T00:00:00',
            '2021-12-02T00:30:00 1',
            '2021-12-02T01:00:00 0',
            '2021-12-02T01:30:00 4',
        ]
        traffic_counter = TrafficCounter()
        for line in input_lines:
            traffic_counter.process_line(line)
        self.assertEqual(traffic_counter.total_cars, 7)
        self.assertDictEqual(traffic_counter.date_total, {
                             '2021-12-01': 2, '2021-12-02': 5})
        self.assertListEqual(
            traffic_counter.get_top_three_record(),
            [
                '2021-12-02T01:30:00 4',
                '2021-12-01T23:00:00 2',
                '2021-12-02T00:30:00 1',
            ]
        )

        self.assertEqual(
            traffic_counter.get_least_count_one_and_half_hour_record(),
            '2021-12-01T23:30:00 1'
        )

    def test_two_day_with_3_gap(self):
        input_lines = [
            '2021-12-01T23:00:00 2',
            # skip a half hour record:      '2021-12-01T23:30:00'
            # skip 2nd half hour record:    '2021-12-02T00:00:00',
            # skip 3rd half hour record     '2021-12-02T00:30:00',
            '2021-12-02T01:00:00 1',
            '2021-12-02T01:30:00 4',
        ]
        traffic_counter = TrafficCounter()
        for line in input_lines:
            traffic_counter.process_line(line)
        self.assertEqual(traffic_counter.total_cars, 7)
        self.assertDictEqual(traffic_counter.date_total, {
                             '2021-12-01': 2, '2021-12-02': 5})
        self.assertListEqual(
            traffic_counter.get_top_three_record(),
            [
                '2021-12-02T01:30:00 4',
                '2021-12-01T23:00:00 2',
                '2021-12-02T01:00:00 1',
            ]
        )

        self.assertEqual(
            traffic_counter.get_least_count_one_and_half_hour_record(),
            '2021-12-01T23:30:00 0'
        )

    def test_less_than_3_records(self):
        input_lines = [
            '2021-12-01T23:00:00 2',
            '2021-12-01T23:30:00 1',
        ]
        traffic_counter = TrafficCounter()
        for line in input_lines:
            traffic_counter.process_line(line)
        self.assertEqual(traffic_counter.total_cars, 3)
        self.assertDictEqual(traffic_counter.date_total, {
                             '2021-12-01': 3})
        self.assertListEqual(
            traffic_counter.get_top_three_record(),
            [
                '2021-12-01T23:00:00 2',
                '2021-12-01T23:30:00 1',
            ]
        )

        with self.assertRaises(Exception) as context:
            traffic_counter.get_least_count_one_and_half_hour_record()
        self.assertEqual(str(context.exception),
                         "TrafficCounter has not process enough records to produce least_count_one_and_half_hour_record")

    def test_sample_input_from_spec(self):
        input_lines = [
            '2021-12-01T05:00:00 5',
            '2021-12-01T05:30:00 12',
            '2021-12-01T06:00:00 14',
            '2021-12-01T06:30:00 15',
            '2021-12-01T07:00:00 25',
            '2021-12-01T07:30:00 46',
            '2021-12-01T08:00:00 42',
            '2021-12-01T15:00:00 9',
            '2021-12-01T15:30:00 11',
            '2021-12-01T23:30:00 0',
            '2021-12-05T09:30:00 18',
            '2021-12-05T10:30:00 15',
            '2021-12-05T11:30:00 7',
            '2021-12-05T12:30:00 6',
            '2021-12-05T13:30:00 9',
            '2021-12-05T14:30:00 11',
            '2021-12-05T15:30:00 15',
            '2021-12-08T18:00:00 33',
            '2021-12-08T19:00:00 28',
            '2021-12-08T20:00:00 25',
            '2021-12-08T21:00:00 21',
            '2021-12-08T22:00:00 16',
            '2021-12-08T23:00:00 11',
            '2021-12-09T00:00:00 4',
        ]
        traffic_counter = TrafficCounter()
        for line in input_lines:
            traffic_counter.process_line(line)
        self.assertEqual(traffic_counter.total_cars, 398)
        self.assertDictEqual(traffic_counter.date_total, {
                             '2021-12-01': 179, '2021-12-05':81, '2021-12-08':134, '2021-12-09': 4 })
        self.assertListEqual(
            traffic_counter.get_top_three_record(),
            [
                '2021-12-01T07:30:00 46',
                '2021-12-01T08:00:00 42',
                '2021-12-08T18:00:00 33',
            ]
        )

        self.assertEqual(
            traffic_counter.get_least_count_one_and_half_hour_record(),
            '2021-12-01T08:30:00 0'
        )


if __name__ == '__main__':
    unittest.main()
