from email import parser
import json
import requests
import argparse
from datetime import datetime
import csv

from tests.bench_mark.func_exec_time_decorator import func_exec_time_decorator

import pdb  # TODO Remove this line

# Silent requests insecure ssl warning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class BenchMark:
    def __init__(self, host, provider, project, platform_code, date_time,
                 depth, bbox, variable=None, column=None, size=20000):
        self.__cdms_domain   = host
        self.__provider      = provider
        self.__project       = project
        self.__platform_code = platform_code

        self.__start_time = date_time[0]
        self.__end_time   = date_time[1]

        self.__min_depth = depth[0]
        self.__max_depth = depth[1]

        self.__min_lat_lon = bbox[:2]
        self.__max_lat_lon = bbox[2:]

        self.__variable    = variable
        self.__columns     = column
        self.__size        = size
        self.__start_index = 0  # Always starts from index 0

    @func_exec_time_decorator
    def __execute_query(self):
        """
        time curl 'https://doms.jpl.nasa.gov/insitu?startIndex=3&itemsPerPage=20&minDepth=-99&variable=relative_humidity&columns=air_temperature&maxDepth=-1&startTime=2019-02-14T00:00:00Z&endTime=2021-02-16T00:00:00Z&platform=3B&bbox=-111,11,111,99'
        :return:
        """
        # rest_keyword = 'query_data_doms_custom_pagination'
        rest_keyword = 'query_data_doms'
        # get_url = f'{self.__cdms_domain}/1.0/{rest_keyword}?startIndex={self.__start_index}&itemsPerPage={self.__size}' \
        get_url = f'{self.__cdms_domain}/1.0/{rest_keyword}?startIndex={self.__start_index}' \
                  f'&provider={self.__provider}' \
                  f'&project={self.__project}' \
                  f'&platform={",".join(self.__platform_code)}' \
                  f'{"" if self.__variable is None else f"&variable={self.__variable}"}' \
                  f'{"" if self.__columns is None else f"&columns={self.__columns}"}' \
                  f'&minDepth={self.__min_depth}&maxDepth={self.__max_depth}' \
                  f'&startTime={self.__start_time.strftime("%Y-%m-%dT%H:%M:%SZ")}&endTime={self.__end_time.strftime("%Y-%m-%dT%H:%M:%SZ")}' \
                  f'&bbox={self.__min_lat_lon[0]},{self.__min_lat_lon[1]},{self.__max_lat_lon[0]},{self.__max_lat_lon[1]}'
        print(get_url)
        response = requests.get(
            url=get_url, verify=False
        )
        if response.status_code > 400:
            raise ValueError(f'wrong status code: {response.status_code}. details: {response.text}')
        return json.loads(response.text), get_url

    @func_exec_time_decorator
    def __execute_query_custom_pagination(self):
        """
        time curl 'https://doms.jpl.nasa.gov/insitu?startIndex=3&itemsPerPage=20&minDepth=-99&variable=relative_humidity&columns=air_temperature&maxDepth=-1&startTime=2019-02-14T00:00:00Z&endTime=2021-02-16T00:00:00Z&platform=3B&bbox=-111,11,111,99'

        :return:
        """
        rest_keyword = 'query_data_doms_custom_pagination'
        get_url = f'{self.__cdms_domain}/1.0/{rest_keyword}?startIndex={self.__start_index}&itemsPerPage={self.__size}' \
                    f'&provider={self.__provider}' \
                    f'&project={self.__project}' \
                    f'&platform={",".join(self.__platform_code)}' \
                    f'{"" if self.__variable is None else f"&variable={self.__variable}"}' \
                    f'{"" if self.__columns is None else f"&columns={self.__columns}"}' \
                    f'&minDepth={self.__min_depth}&maxDepth={self.__max_depth}' \
                    f'&startTime={self.__start_time.strftime("%Y-%m-%dT%H:%M:%SZ")}&endTime={self.__end_time.strftime("%Y-%m-%dT%H:%M:%SZ")}' \
                    f'&bbox={self.__min_lat_lon[1]},{self.__min_lat_lon[0]},{self.__max_lat_lon[1]},{self.__max_lat_lon[0]}'
        print(get_url)
        response = requests.get(url=get_url, verify=False)
        if response.status_code > 400:
            raise ValueError(f'wrong status code: {response.status_code}. details: {response.text}')
        return json.loads(response.text), get_url

    @func_exec_time_decorator
    def __execute_blind_query(self, get_url):
        """
        :return:
        """
        print(get_url)
        response = requests.get(url=get_url, verify=False)
        if response.status_code > 400:
            raise ValueError(f'wrong status code: {response.status_code}. details: {response.text}')
        return json.loads(response.text), get_url

    @func_exec_time_decorator
    def __execute_query_custom_pagination_paginate(self, markerTime, markerPlatform):
        """
        time curl 'https://doms.jpl.nasa.gov/insitu?startIndex=3&itemsPerPage=20&minDepth=-99&variable=relative_humidity&columns=air_temperature&maxDepth=-1&startTime=2019-02-14T00:00:00Z&endTime=2021-02-16T00:00:00Z&platform=3B&bbox=-111,11,111,99'

        :return:
        """
        rest_keyword = 'query_data_doms_custom_pagination'
        get_url = f'{self.__cdms_domain}/1.0/{rest_keyword}?startIndex={self.__start_index}&itemsPerPage={self.__size}' \
                  f'&provider={self.__provider}' \
                  f'&markerTime={markerTime}' \
                  f'&markerPlatform={markerPlatform}' \
                  f'&project={self.__project}' \
                  f'&platform={self.__platform_code}' \
                  f'{"" if self.__variable is None else f"&variable={self.__variable}"}' \
                  f'{"" if self.__columns is None else f"&columns={self.__columns}"}' \
                  f'&minDepth={self.__min_depth}&maxDepth={self.__max_depth}' \
                  f'&startTime={self.__start_time}&endTime={self.__end_time}' \
                  f'&bbox={self.__min_lat_lon[0]},{self.__min_lat_lon[1]},{self.__max_lat_lon[0]},{self.__max_lat_lon[1]}'
        # rest_keyword = 'query_data_doms'
        print(get_url)
        response = requests.get(url=get_url, verify=False)
        if response.status_code > 400:
            raise ValueError(f'wrong status code: {response.status_code}. details: {response.text}')
        return json.loads(response.text)

    def pagination_benchmark(self):
        header = ['url', 'count', 'duration']
        rows   = []

        # Initial request
        # response, url = self.__execute_query_custom_pagination()
        response, duration, execution_times = self.__execute_query_custom_pagination()
        rows.append([
            response[1],
            len(response[0]["results"]),
            duration
        ])

        while response[0]['next'] != 'NA':
            if len(response[0]['results']) < 1:
                print('empty result set. breaking')
                break

            # Subsequent request(s) to get next page
            response, duration, execution_times = self.__execute_blind_query(response[0]['next'])
            rows.append([
                response[1],
                len(response[0]["results"]),
                duration
            ])

        return header, rows

    def time_benchmark(self):
        """
time: 2017-01-01T00:00:00Z - 2017-01-02T00:00:00Z -- total: 8316 -- duration: 105.139927
time: 2017-12-01T00:00:00Z - 2017-12-16T00:00:00Z -- total: 59753 -- duration: 72.037163
time: 2017-02-01T00:00:00Z - 2017-02-28T00:00:00Z -- total: 104602 -- duration: 67.783443
time: 2017-04-01T00:00:00Z - 2017-05-30T00:00:00Z -- total: 380510 -- duration: 112.183817
time: 2017-06-01T00:00:00Z - 2017-08-30T00:00:00Z -- total: 661753 -- duration: 145.768916
time: 2017-01-01T00:00:00Z - 2017-06-30T00:00:00Z -- total: 979690 -- duration: 251.343631

        :return:
        """
        
        header = ['url', 'count', 'duration']
        rows   = []

        # print( f'time: {self.__start_time} - {self.__end_time} -- total: {response[0]["total"]} -- duration: {response[1]}' )

        response, duration, execution_times = self.__execute_query()
        rows.append([
            response[1],
            len(response[0]["results"]),
            duration
        ])
        return header, rows

    def depth_bench_mark(self):
        return

    def bbox_bench_mark(self):
        return

    def samos_test(self):
        """
        provider=Florida State University, COAPS/
project=SAMOS/
platform_code=30/
        :return:
        """
        self.__variable = 'relative_humidity'
        self.__columns = None
        self.__start_time = '2017-01-01T00:00:00Z'
        self.__end_time = '2017-01-03T00:00:00Z'
        self.__min_depth = -99
        self.__max_depth = 0
        self.__min_lat_lon = (-111, 11)
        self.__max_lat_lon = (111, 99)
        self.__provider = 'Florida State University, COAPS'
        self.__project = 'SAMOS'
        self.__platform_code = '301'
        print(self.__execute_query())
        return


def init_argparse():

    # ArgumentParser datetime type validation
    def valid_datetime(dt):
        try:
            return datetime.strptime(dt, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            raise argparse.ArgumentTypeError(f'Not a valid date: {dt}')

    parser = argparse.ArgumentParser(description="Benchmark test against SDAP In-situ")
    parser.add_argument(
        '-s', '--host', type=str, required=True,
        help="Hostname to the SDAP In-situ data service node")
    parser.add_argument(
        '-r', '--provider', type=str, required=True,
        help="Data provider")
    parser.add_argument(
        '-p', '--project', type=str, required=True,
        help="Project name")
    parser.add_argument(
        '-c', '--platform-code', type=str, required=True, nargs='+',
        help="Platform code: {code}+")
    parser.add_argument(
        '-t', '--date-time', type=valid_datetime, required=True, nargs=2,
        help="Datetime: {start_datetim} {end_datetime}")
    parser.add_argument(
        '-d', '--depth', type=int, required=True, nargs=2,
        help="Depth min and max: {min_depth} {max_depth}")
    parser.add_argument(
        '-b', '--bbox', type=int, required=True, nargs=4,
        help="Bounding box: {min_lat} {min_lon} {max_lat} {max_lon}")
    parser.add_argument(
        '-e', '--benchmark', type=str, required=True,
        help="Select benchmark test: [{pagination_benchmark}]")
    parser.add_argument(
        '-o', '--output-file', type=str, required=True,
        help="CSV output file destination: {full_path}/{CSV_filename}")

    return parser.parse_args()
            

if __name__ == '__main__':
    # Parse cli argument 
    args = init_argparse()

    # Pick benchmark test
    bm = BenchMark(
        host=f'https://{args.host}/insitu',
        provider=args.provider,
        project=args.project,
        platform_code=args.platform_code,
        date_time=args.date_time,
        depth=args.depth,
        bbox=args.bbox
    )
    if args.benchmark == 'pagination_benchmark':
        csv_header, csv_rows = bm.pagination_benchmark()
    elif args.benchmark == 'time_benchmark':
        csv_header, csv_rows = bm.time_benchmark()
    else:
        print(f'Invalid benchmark test selection')
        exit(1)

    # Write to CSV file
    with open(args.output_file, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(csv_header)
        csv_writer.writerows(csv_rows)
