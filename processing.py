"""
Allen Yu, Lilah Favour

This program implements functions that does
data analysis and visualization on Twitch data.
"""

import pandas as pd
import glob
import datetime
from dateutil.relativedelta import relativedelta


def combine_csv(channel_dict):
    """
    Takes in a dictionary channel_dict and
    combined all related csv files into one.
    """
    for channel_name in channel_dict.keys():
        streamer_path = '/home/data/' + channel_name + '/'
        all_filenames = [i for i in
                         glob.glob(streamer_path + '*.{}'.format('csv'))]
        all_filenames.sort()

        export_path = '/home/data/combined/'
        export_name = channel_name + "_combined.csv"
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
        combined_csv.to_csv(export_path + export_name,
                            index=False, encoding='utf-8-sig')


def agg_columns(csv_path):
    """
    Takes in a string representing the
    CSV file path and return a DataFrame with
    columns filtered.
    """
    df = pd.read_csv(csv_path)

    raw_time = df["Stream start time"].str.split(" ")
    format_time = []

    for index, value in raw_time.items():
        time = value[2] + " " + value[3]
        format_time.append(time)
    df["Stream month"] = format_time

    df = df[['Stream month', 'Avg viewers', 'Peak viewers']]
    df = df.groupby('Stream month', sort=False)
    df = df.agg({'Avg viewers': 'mean', 'Peak viewers': 'max'})

    return df


def get_time_range(start_m, start_y, end_m, end_y):
    """
    Takes in 4 integers, start month, start year,
    end month, and end year. Return a list within
    a range of time.
    """
    result = []

    end = datetime.date(end_y, end_m, 1)
    start = datetime.date(start_y, start_m, 1)

    while start <= end:
        year = str(start.year)
        month = start.strftime("%B").lower()
        result.append(year + month)
        start += relativedelta(months=1)

    return result
