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

from pyspark.sql.types import StructType, StructField, DoubleType, \
    StringType, MapType, LongType, TimestampType, IntegerType

class CdmsSchema:
    ALL_SCHEMA = StructType([
        # Common
        StructField('provider', StringType(), True),
        StructField('project', StringType(), True),
        StructField('time', StringType(), True),
            StructField('time_obj', TimestampType(), True),
        StructField('latitude', DoubleType(), True),
        StructField('longitude', DoubleType(), True),
        StructField('site', StringType(), True),

        # AQ
        StructField('pm2_5', DoubleType(), True),
        StructField('bc', DoubleType(), True),
        StructField('no2', DoubleType(), True),
        StructField('co', DoubleType(), True),
        StructField('co2', DoubleType(), True),
        StructField('no', DoubleType(), True),
        StructField('o3', DoubleType(), True),
        StructField('pm1', DoubleType(), True),
        StructField('pm10', DoubleType(), True),
        StructField('pm25', DoubleType(), True),

        # IDEAS
        StructField('Qout', DoubleType(), True),
        StructField('Streamflow', DoubleType(), True),
        StructField('Gage_height', DoubleType(), True),
        StructField('Stream_water_level_elevation_above_NAVD_1988', DoubleType(), True),
        StructField('Lake_or_reservoir_water_surface_elevation_above_NAVD_1988', DoubleType(), True),
        StructField('Temperature', DoubleType(), True),
        StructField('Spcific_conductance', DoubleType(), True),
        StructField('Turbidity', DoubleType(), True),
        StructField('Suspended_sediment_concentration', DoubleType(), True),
        StructField('Precipitation', DoubleType(), True),
        StructField('Depth_to_water_level', DoubleType(), True),
        StructField('Streamflow_quality', StringType(), True),
        StructField('Gage_height_quality', StringType(), True),
        StructField('Stream_water_level_elevation_above_NAVD_1988_quality', StringType(), True),
        StructField('Lake_or_reservoir_water_surface_elevation_above_NAVD_1988_quality', StringType(), True),
        StructField('Temperature_quality', StringType(), True),
        StructField('Specific_conductance_quality', StringType(), True),
        StructField('Turbidity_quality', StringType(), True),
        StructField('Suspended_sediment_concentration_quality', StringType(), True),
        StructField('Precipitation_quality', StringType(), True),
        StructField('Depth_to_water_level_quality', StringType(), True),
        StructField('vortex_height', DoubleType(), True),
        StructField('vortex_avg_speed', DoubleType(), True),
        StructField('vortex_height_rise_speed', DoubleType(), True),
        StructField('vortex_rain', DoubleType(), True)
    ])
