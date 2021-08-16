"""
Allen Yu, Lilah Favour

This program implements functions that does
data analysis and visualization on Twitch data.
"""

import pandas as pd
import re
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from processing import agg_columns, get_time_range

sns.set()


def viewers_vs_games(channel_dict):
    """
    Takes in a dictionary channel_dict and
    plot the it plots games based on average viewers
    and stream time for each individual channel.
    """
    for lower_name, og_name in channel_dict.items():
        csv_path = '/home/data/' + lower_name + '/' + \
                    lower_name + '_game.csv'
        df = pd.read_csv(csv_path)

        raw_game = df["Game"].str.split("|")
        format_game = []

        for index, value in raw_game.items():
            game = value[0].strip()
            format_game.append(game)
        df["Game played"] = format_game
        df = df[['Game played', 'Stream time', 'Average viewers']]
        df = df.iloc[:10]

        sns.relplot(x='Stream time', y='Average viewers',
                    data=df, hue='Game played')
        plt.xlabel('Time in Minutes')
        plt.ylabel('Average Viewers')
        plt.title('Game data for ' + og_name)

        plt.savefig('/home/viewers_vs_games_' +
                    lower_name + '.png', bbox_inches='tight')


def covid_impact(channel_dict):
    """
    Takes in a dictionary channel_dict and plot
    the data that shows how the pandamic shapes
    the entirely of Twitch, and the individual streamers.
    """
    custom_time_data(1, 2019, 2, 2021)

    for lower_name, og_name in channel_dict.items():
        fig, ax = plt.subplots(1, figsize=(20, 10))

        csv_path = '/home/data/combined/' + lower_name + '_combined.csv'
        df = agg_columns(csv_path)

        df['Stream month'] = df.index
        df.plot(x='Stream month', y='Peak viewers',
                ax=ax, kind='bar', color='#add8e6')
        df.plot(x='Stream month', y='Avg viewers',
                ax=ax, kind='bar', color='#9370DB')

        plt.title(og_name)
        plt.xlabel('Time in Months')
        plt.ylabel('Viewers')
        plt.xticks(rotation=45)
        plt.gca().invert_xaxis()

        output_name = lower_name + '_impact.png'
        fig.savefig('/home/' + output_name)


def custom_time_data(start_m, start_y, end_m, end_y):
    """
    Takes in 4 integers, start month, start year,
    end month, and end year. Then scrape the data
    from a specific time frame and plot both average
    viewers and peak viewers.
    """
    url = "https://sullygnome.com/"

    time_range = get_time_range(start_m, start_y, end_m, end_y)
    index_time = []
    avg_viewers_data = []
    peak_viwers_data = []
    for time in time_range:
        curr_url = url + time
        year_month = re.findall(r'[A-Za-z]+|\d+', time)

        month = year_month[1].capitalize()
        date = datetime.datetime.strptime(month, "%B")
        month = date.strftime("%b")

        format_time = (month + ' ' + year_month[0][2:])

        soup = get_soup(curr_url)
        monthy_data = soup.find_all('div', class_='InfoStatPanelTLCell')

        avg_viewers = int(re.sub("[^0-9]", "", monthy_data[1].get_text()))
        peak_viewers = int(re.sub("[^0-9]", "", monthy_data[2].get_text()))

        index_time.append(format_time)
        avg_viewers_data.append(avg_viewers)
        peak_viwers_data.append(peak_viewers)

    df_avg_viewers = pd.DataFrame({'Avg viewers': avg_viewers_data},
                                  index=index_time)
    df_peak_viewers = pd.DataFrame({'Peak viewers': peak_viwers_data},
                                   index=index_time)

    fig, ax = plt.subplots(1, figsize=(20, 10))

    df_peak_viewers.plot(ax=ax, kind='bar', color='#add8e6')
    df_avg_viewers.plot(ax=ax, kind='bar', color='#9370DB')

    plt.title('Total Twitch Viewers Over Time')
    plt.xlabel('Time in Months')
    plt.ylabel('Viewers in Millions')
    plt.xticks(rotation=45)

    fig.savefig('/home/custom_time_data.png')


def get_soup(url):
    """
    Takes in a string URL and returns
    the soup object for web scraping purposes.
    """
    user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  'AppleWebKit/537.36 (KHTML, like Gecko'
                  'Chrome/89.0.4389.82 Safari/537.36')
    req = Request(url, headers={'User-agent': user_agent})
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')

    return soup


def yearly_growth_rate(channel_dict):
    """
    Takes in a dictionary channel_dict and returns
    the growth rate of average viewers for that
    channel over the last 12 months. If the channel
    hasn't been active for that long, it calculates
    from the earliest month available.
    """
    for lower_name, og_name in channel_dict.items():
        csv_path = '/home/data/combined/' + lower_name + '_combined.csv'

        df = agg_columns(csv_path)
        df = df.loc[~df.index.str.endswith('2019')]
        data = df.iloc[[0, -1]]['Avg viewers'].to_dict()

        first_month = list(data)[1]
        recent_month = list(data)[0]
        first_month_n = int(list(data.values())[1])
        recent_month_n = int(list(data.values())[0])

        percent = str(round(((recent_month_n - first_month_n) /
                            first_month_n) * 100, 2))
        result = "The growth rate for " + og_name + \
            " from " + first_month + " to " + recent_month + \
            " is " + percent + "%"
        print(result)


def main():
    channel_dict = {'jacksepticeye': 'jacksepticeye',
                    'karljacobs': 'karljacobs',
                    'philza': 'Philza', 'pokimane': 'Pokimane',
                    'ranboolive': 'RanbooLive', 'sapnap': 'Sapnap',
                    'sykkuno': 'Sykkuno', 'tommyinnit': 'tommyinnit',
                    'tubbo': 'Tubbo', 'wilbursoot': 'WilburSoot'}

    yearly_growth_rate(channel_dict)
    #viewers_vs_games(channel_dict)
    #covid_impact(channel_dict)


if __name__ == "__main__":
    main()
