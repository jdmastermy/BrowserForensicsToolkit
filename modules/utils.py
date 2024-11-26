
import csv
from datetime import datetime, timedelta

def convert_webkit_time(microseconds):
    epoch_start = datetime(1601, 1, 1)
    delta = timedelta(microseconds=microseconds)
    return (epoch_start + delta).strftime('%Y-%m-%d %H:%M:%S')

def convert_firefox_time(milliseconds):
    return datetime.utcfromtimestamp(milliseconds / 1000000).strftime('%Y-%m-%d %H:%M:%S')

def write_to_csv(data, headers, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)
