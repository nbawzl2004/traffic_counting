'''
Module for TrafficCounter
'''

from typing import List, Tuple, Optional, Dict
from datetime import datetime, timedelta


class TrafficCounter:
    '''
    Class to count traffcs
    '''
    HALF_HOUR_IN_SECONDS = 1800

    def __init__(self):
        # The number of cars seen in total
        self.total_cars: int = 0
        #  A sequence of lines where each line contains a date (in yyyy-mm-dd format) and the
        #    number of cars seen on that day (eg. 2016-11-23 289)
        #    for all days listed in the input file.
        self.date_total: Dict[str, int] = {}
        # The top 3 half hours with most cars, in the same format as the input file.
        # The Length is <= 3. Tuple[count on that record, record]
        self.top_three_record: List[Tuple[int, str]] = []

        # The 1.5 hour period with least cars. Tuple[car counts, starting record]
        # self.least_car_one_and_half_hour: Optional[Tuple[int, str]] = None

        # Holding counts for the last 3 contiguous half hours. The Length is <= 3.
        self.last_three_half_hours_count: List[int] = []
        # last processed record timestmap.
        self.last_processed_datetime: Optional[datetime] = None

        # stores the min result of count for 3 contiguous half hours and the starting time.
        self.min_one_and_half_hour_count: Optional[Tuple[int, datetime]] = None

    def get_top_three_record(self) -> List[str]:
        '''
        return The top 3 half hours record with most cars, in the same format as the input file
        '''
        return list(map(lambda record_tuple: record_tuple[1] + " " + str(record_tuple[0]), self.top_three_record))

    def get_least_count_one_and_half_hour_record(self) -> str:
        '''
        return string contains a record showing information about
           The 1.5 hour period with least cars (i.e. 3 contiguous half hour records)
           format in "starting-time 1.5hour-count"
           eg: 2021-12-01T23:00:00 31, mean from 2021-12-01T23:00:00
           to 2021-12-02T00:30:00 (total 1.5 hours), there are 1.5hour-count cars
        '''
        if len(self.last_three_half_hours_count) < 3:
            raise Exception(
                "TrafficCounter has not process enough records to produce least_count_one_and_half_hour_record")

        return self.min_one_and_half_hour_count[1].isoformat() + " " + str(self.min_one_and_half_hour_count[0])

    def process_line(self, line: str) -> None:
        '''
        @line: input line from the file. should be in format like
            2021-12-01T05:00:00 5
        '''
        (time_str, count_str) = line.split(" ")
        current_record_count = int(count_str)
        current_record_datetime = datetime.fromisoformat(time_str)

        # process record for total cars
        self.total_cars += current_record_count

        # process record for date total
        date_str = f"{current_record_datetime:%Y-%m-%d}"
        if date_str in self.date_total:
            self.date_total[date_str] += current_record_count
        else:
            self.date_total[date_str] = current_record_count

        self.__process_top_three_record(current_record_count, time_str)
        self.__process_least_count_one_and_half_hour(
            current_record_datetime, current_record_count)

    def __process_least_count_one_and_half_hour(self, current_record_datetime: datetime, count: int):
        if self.min_one_and_half_hour_count and self.min_one_and_half_hour_count[0] == 0:
            # has already found one_and_half hour with 0 traffic. Don't need to run again,
            # because we have already found the smallest
            return

        if self.last_processed_datetime:
            delta = current_record_datetime - self.last_processed_datetime
            if delta.total_seconds() > self.HALF_HOUR_IN_SECONDS * 3:
                # There 3 empty records
                self.last_three_half_hours_count = [0, 0, 0]
                next_half_hour = self.last_processed_datetime + \
                    timedelta(seconds=self.HALF_HOUR_IN_SECONDS)
                self.min_one_and_half_hour_count = (
                    0, next_half_hour)
            else:
                # Less than 3 empty records
                to_process_datetime = self.last_processed_datetime + \
                    timedelta(seconds=self.HALF_HOUR_IN_SECONDS)
                while to_process_datetime <= current_record_datetime:
                    current_virtual_record_count = 0
                    if to_process_datetime == current_record_datetime:
                        current_virtual_record_count = count
                    if len(self.last_three_half_hours_count) < 3:
                        # processed less than 3 records (including the current one)
                        self.last_three_half_hours_count.append(
                            current_virtual_record_count)
                        self.min_one_and_half_hour_count = (
                            self.min_one_and_half_hour_count[0] +
                            current_virtual_record_count, self.min_one_and_half_hour_count[1])
                    else:
                        # have process more than 3 records
                        self.last_three_half_hours_count.pop(0)
                        self.last_three_half_hours_count.append(
                            current_virtual_record_count)
                        last_three_half_hour_sum = sum(
                            self.last_three_half_hours_count)
                        if last_three_half_hour_sum < self.min_one_and_half_hour_count[0]:
                            self.min_one_and_half_hour_count = (
                                last_three_half_hour_sum,
                                to_process_datetime -
                                timedelta(seconds=self.HALF_HOUR_IN_SECONDS * 2))
                    to_process_datetime = to_process_datetime + \
                        timedelta(seconds=self.HALF_HOUR_IN_SECONDS)
        else:
            # first record being processed
            self.last_three_half_hours_count.append(count)
            self.min_one_and_half_hour_count = (count, current_record_datetime)

        self.last_processed_datetime = current_record_datetime

    def __process_top_three_record(self, current_record_count: int, time_str: str):
        if len(self.top_three_record) < 3:
            # top_three_record not full yet
            self.top_three_record.append((current_record_count, time_str))
            self.__sort_top_three_record()
        else:
            # top_three_record not full
            if current_record_count > self.top_three_record[2][0]:
                # new record should be added to top 3
                self.top_three_record[2] = (current_record_count, time_str)
                self.__sort_top_three_record()

    def __sort_top_three_record(self):
        for i in range(len(self.top_three_record)-1, 0, -1):
            if self.top_three_record[i-1][0] < self.top_three_record[i][0]:
                self.top_three_record[i - 1], self.top_three_record[i] = \
                    self.top_three_record[i], self.top_three_record[i-1]
