import numpy as np
import pandas as pd
from pandas import DataFrame

# 'https://files.airnowtech.org/?prefix=airnow/'
class DownloadRawData:
    def __init__(self, download_dir='/tmp'):
        self.__download_dir = download_dir
        self.base_url = 'https://s3-us-west-1.amazonaws.com//files.airnowtech.org/airnow'

    def get_one_file(self, incoming_url) -> DataFrame:
        try:
            data = pd.read_csv(incoming_url, sep='|', encoding='latin1', header=None)
        except Exception as e:
            print(f'Error getting data for {incoming_url}. {e}')
            raise e
        return data

    def download_one_file(self, current_hour: int, current_date) -> DataFrame:
        date_str = str(current_date).replace('-', '')
        date_time_str = f'{current_date}T{current_hour:02d}:00:00Z'
        hourly_url = f'{self.base_url}/{date_str[:4]}/{date_str}/HourlyData_{date_str}{str(current_hour).rjust(2, "0")}.dat'
        filename = f'{date_str}_{str(current_hour).rjust(2, "0")}.csv'
        hourly_data = self.get_one_file(hourly_url)
        hourly_data = hourly_data[[2, 5, 7]]
        hourly_data.columns = ['site_id', 'name', 'value']
        hourly_data = hourly_data.pivot_table(index='site_id', columns='name', values='value', aggfunc='mean').reset_index()
        hourly_data['time'] = date_time_str
        keeping_columns = ['site_id', 'time']
        data_columns = ['CO', 'NO2', 'NO', 'SO2', 'PM2.5', 'PM10', 'OZONE']
        data_columns = [k for k in data_columns if k in hourly_data]
        keeping_columns = keeping_columns + data_columns
        hourly_data = hourly_data[keeping_columns]
        """
                    'OZONE': 'o3',
            'CO': 'co',
            # 'NO': 'no',
            'NO2': 'no2',
            'SO2': 'so2',
            'PM25': 'pm2_5',
            'PM10': 'pm10',
        """
        return hourly_data

    def download_data(self, start_date: str, end_date: str):
        start_date = np.datetime64(start_date)
        end_date = np.datetime64(end_date)
        dates = np.arange(start_date, end_date)
        for date in dates:
            scoordinate_data = self.download_coordinate(date)
            for i in range(24):
                hourly_data = self.download_one_file(i, date)
                hourly_data = hourly_data.merge(scoordinate_data, on='site_id', how='left')
                filename = f'{str(date)}_{str(i).rjust(2, "0")}.csv'
                hourly_data.to_csv(f'{self.__download_dir}/{filename}', index=False)
        return

    def download_coordinate(self, current_date: str):
        date_str = str(current_date).replace('-', '')
        date_time_str = f'{current_date}T00:00:00Z'
        coordiniate_url = f'{self.base_url}/{date_str[:4]}/{date_str}/monitoring_site_locations.dat'
        try:
            coordinate_data = pd.read_csv(coordiniate_url, sep='|', encoding='latin1', header=None)
            coordinate_data = coordinate_data[[0, 8, 9]]
            coordinate_data.columns = ['site_id', 'lat', 'lon']
            # coordinate_data['time'] = date_time_str
            # filename = f'{date_str}_coordinates.csv'
            # coordinate_data.to_csv(f'{self.__download_dir}/{filename}', index=False)
        except Exception as e:
            print(f'Error getting data for {coordiniate_url}. {e}')
            raise e
        return coordinate_data

    def download_coordinates(self, start_date: str, end_date: str):
        start_date = np.datetime64(start_date)
        end_date = np.datetime64(end_date)
        dates = np.arange(start_date, end_date)
        for date in dates:
            self.download_coordinate(date)
        return

# DownloadRawData().download_coordinates('2021-06-01', '2021-06-05')
DownloadRawData().download_data('2021-06-01', '2021-06-05')
