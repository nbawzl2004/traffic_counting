'''
This module read input file and use TrafficCounter to count traffics
'''
import sys
from io import BufferedReader
from os.path import exists as path_exists
from traffic_counter import TrafficCounter


def validate_input() -> None:
    '''
    Validates input of the problem.
    '''
    if len(sys.argv) > 2:
        sys.exit(
            "Too many arguments passed in. You should only pass in 1 input file.")
    if len(sys.argv) < 2:
        sys.exit(
            "No file path passed in. You should pass in exactly 1 input file.")


def get_file_object() -> BufferedReader:
    '''
    Check file path and return the opened file object
    '''
    filename = sys.argv[1]
    if not path_exists(filename):
        sys.exit(
            "The file path: " + filename + " does not exists. Please pass in a valid path.")
    return open(filename, "r", encoding="utf-8")


def main() -> None:
    '''
    Program Entrance
    '''
    validate_input()
    input_file = get_file_object()
    line_count = 0
    traffic_counter = TrafficCounter()
    for line in input_file:
        line_count += 1
        traffic_counter.process_line(line)

    print(f"Processed {line_count} lines from input file: {sys.argv[1]}.")
    print(f"There are {traffic_counter.total_cars} cars in total.")
    print("Following is a breakdown by date:")
    print("...", traffic_counter.date_total)
    print("Following are the top 3 half hours with most cars:")
    print("...", traffic_counter.get_top_three_record())
    print("Following is the 1.5 hour period with least cars and count")
    print("...", traffic_counter.get_least_count_one_and_half_hour_record())


if __name__ == "__main__":
    main()
