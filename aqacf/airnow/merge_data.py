import os
from datetime import datetime
from glob import glob
import pandas as pd

from parquet_flask.utils.file_utils import FileUtils


class MergeData:
    def __init__(self, raw_data_dir: str, merged_data_dir: str):
        self.__raw_data_dir = raw_data_dir
        self.__merged_data_dir = merged_data_dir

    def start(self):
        cs_files = glob(os.path.join(self.__raw_data_dir, '*.csv'))
        data_frames = [pd.read_csv(each_file, sep=',', encoding='latin1') for each_file in cs_files]
        concat_data_frame = pd.concat(data_frames, axis=0)
        concat_data_frame.sort_values(by=['site_id', 'time'], ascending=[True, True], inplace=True)
        FileUtils.mk_dir_p(self.__merged_data_dir)
        concat_data_frame.to_csv(os.path.join(self.__merged_data_dir, 'raw.csv'), index=False)
        concat_data_frame['time'] = pd.to_datetime(concat_data_frame['time'])
        data_columns = set(concat_data_frame.columns.tolist())
        data_columns.remove('site_id')
        data_columns.remove('time')
        result_df = concat_data_frame.groupby(['site_id', concat_data_frame['time'].dt.date])[list(data_columns)].mean().reset_index()
        result_df.to_csv(os.path.join(self.__merged_data_dir, 'daily.csv'), index=False)
        return

time1 = datetime.now()
# MergeData('/tmp/airnow2', '/tmp/airnow2/concat').start()
time2 = datetime.now()
print(time2 - time1)
