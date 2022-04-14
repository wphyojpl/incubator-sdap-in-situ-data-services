import unittest

from parquet_flask.io_logic.partitioned_parquet_path import PartitionedParquetPath


class TestGeneralUtilsV3(unittest.TestCase):
    def test_01(self):
        first = PartitionedParquetPath('my_base').set_provider('abc').set_project('def').set_platform('ghi').set_year('2001').set_month('02').set_lat_lon((3,4))
        second = first.duplicate().set_year('2012').set_lat_lon((5,-8))
        third = first.duplicate().set_platform(None)
        self.assertEqual(first.generate_path(), 'my_base/provider=abc/project=def/platform_code=ghi/geo_spatial_interval=3_4/year=2001/month=02', 'wrong path')
        self.assertEqual(second.generate_path(), 'my_base/provider=abc/project=def/platform_code=ghi/geo_spatial_interval=5_-8/year=2012/month=02', 'wrong path')
        self.assertEqual(third.generate_path(), 'my_base/provider=abc/project=def', 'wrong path')
        return
