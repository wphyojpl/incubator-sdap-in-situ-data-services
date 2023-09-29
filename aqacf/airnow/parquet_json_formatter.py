import multiprocessing
multiprocessing.set_start_method("fork")

import os
from copy import deepcopy

import numpy as np
import pandas as pd

from parquet_flask.utils.file_utils import FileUtils


def process_dict(data_dict_input):
    data_dict = deepcopy(data_dict_input)
    removing_keys = [k for k, v in data_dict.items() if not isinstance(v, str) and np.isnan(v)]
    data_dict['platform'] = {
        'id': data_dict['id'],
        'short_name': data_dict['short_name'] if 'short_name' in data_dict else '',
    }
    removing_keys += ['id', 'short_name']
    for k in removing_keys:
        if k in data_dict:
            data_dict.pop(k)
    return data_dict

class ParquetJsonFormatter:
    def __init__(self, provider_name: str, project_name):
        self.__provider_name = provider_name
        self.__project_name = project_name

    def start(self, csv_file: str):
        airnow_data = pd.read_csv(csv_file, sep=',', encoding='latin1')
        """
        {
          "time": "2023-01-01T04:00:00Z",
          "latitude": 34.1439,
          "longitude": -117.8508,
          "o3": 19.0,
          "co": 0.1,
          "no": 0.0,
          "no2": 2.2,
          "pm2_5": 0.0,
          "platform": {
            "id": "060370016",
            "short_name": "Glendora - Laurel"
          }
      site_id,time,CO,NO2,NO,SO2,PM2.5,PM10,OZONE,site_name,lat,lon
        """
        renaming_column_dict = {
            'site_id': 'id',
            'site_name': 'short_name',
            'lat': 'latitude',
            'lon': 'longitude',
            'OZONE': 'o3',
            'CO': 'co',
            'NO': 'no',
            'NO2': 'no2',
            'SO2': 'so2',
            'SO3': 'so2',
            'PM2.5': 'pm2_5',
            'PM10': 'pm10',
        }
        airnow_data.rename(columns=renaming_column_dict, inplace=True)
        # airnow_data.fillna(None, inplace=True)

        json_list = airnow_data.to_dict(orient='records')
        pool = multiprocessing.Pool()

        # Use the Pool to apply the process_dict function to each dictionary in parallel
        result_list = pool.map(process_dict, json_list)
        # Close the Pool
        pool.close()
        pool.join()
        site_json = {
            "project": self.__project_name,
            "provider": self.__provider_name,
            "observations": result_list
        }
        FileUtils.write_json(f'{csv_file}.json', site_json, overwrite=True, prettify=True)
        return


ParquetJsonFormatter('AirNow', 'air_quality').start('/tmp/airnow3/concat/daily.csv')