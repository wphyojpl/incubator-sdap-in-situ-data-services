# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from parquet_flask.io_logic.partitioned_parquet_path import PartitionedParquetPath

partitioning_column_example = [
    "provider",
    "project",
    "platform_code",
    "geo_spatial_interval",
    "year",
    "month",
    "job_id"
  ]

class TestGeneralUtilsV3(unittest.TestCase):
    def test_dummy(self):
        return
    def test_01(self):
        sample_es_1 = {
            'geo_spatial_interval': '3_4',
            'provider': 'abc',
            'project': 'def',
            'platform_code': 'ghi',
            'year': '2001',
            'month': '02',
        }
        sample_es_2 = {
            'geo_spatial_interval': '5_-8',
            'provider': 'abc',
            'project': 'def',
            'platform_code': 'ghi',
            'year': '2012',
            'month': '02',
        }
        sample_es_3 = {
            'geo_spatial_interval': '5_-8',
            'provider': 'abc',
            'project': 'def',
            'year': '2012',
            'month': '02',
        }
        first = PartitionedParquetPath('my_base', partitioning_column_example).load_from_es(sample_es_1)
        second = first.duplicate().load_from_es(sample_es_2)
        third = first.duplicate().load_from_es(sample_es_3)
        self.assertEqual(first.generate_path(), 'my_base/provider=abc/project=def/platform_code=ghi/geo_spatial_interval=3_4/year=2001/month=02', 'wrong path')
        self.assertEqual(second.generate_path(), 'my_base/provider=abc/project=def/platform_code=ghi/geo_spatial_interval=5_-8/year=2012/month=02', 'wrong path')
        self.assertEqual(third.generate_path(), 'my_base/provider=abc/project=def', 'wrong path')
        return

    def test_04(self):
        es_result = {
    "s3_url": "s3://cdms-dev-in-situ-parquet/CDMS_insitu.geo2.parquet/provider=Florida State University, COAPS/project=SAMOS/platform_code=30/geo_spatial_interval=-25_150/year=2017/month=6/job_id=6f33d0e5-65ca-4281-b4df-2d703adee683/part-00000-9cfcbe81-3ca9-4084-9b8c-db451bd8c076.c000.gz.parquet",
    "bucket": "cdms-dev-in-situ-parquet",
    "name": "part-00000-9cfcbe81-3ca9-4084-9b8c-db451bd8c076.c000.gz.parquet",
    "provider": "Florida State University, COAPS",
    "project": "SAMOS",
    "platform_code": "30",
    "geo_spatial_interval": "-25_150",
    "year": "2017",
    "month": "6",
    "total": 8532,
    "min_datetime": 1497312000,
    "max_datetime": 1497398340,
    "min_depth": -31.5,
    "max_depth": 5.9,
    "min_lat": -23.8257,
    "max_lat": -23.6201,
    "min_lon": 154.4868,
    "max_lon": 154.6771
  }
        first = PartitionedParquetPath('my_base', partitioning_column_example).load_from_es(es_result)
        self.assertEqual(first.generate_path(), 'my_base/provider=Florida State University, COAPS/project=SAMOS/platform_code=30/geo_spatial_interval=-25_150/year=2017/month=6', 'wrong path')
        return


