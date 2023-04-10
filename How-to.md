This document describes how to create a new data system. 
This system is split into 5 different sections.
- Data
- Data Ingestion
- Metadata Ingestion
- Data Statistics Query
- Data Query
### Data
First of all, a data schema is needed for the system. 
Currently the system supports ingestion of json data documents. 
Examples JSON data document:
- Sample JSON data document in ocean monitoring system

        {
            "provider": "JPL",
            "project": "CDMS",
            "data": [
                {
                    "temperature": 0.5,
                    "temperature_quality": 1,
                    "pressure": 0.0,
                    "pressure_quality": 3,
                    "latitude": 90.112,
                    "longitude": 93.257,
                    "depth": -11.3578,
                    "time": "2021-01-01T00:00:00"
                }
            ]
        }
- Sample JSON data document in spacecraft engineering system

        {
            "mission": "MER",
            "spacecraft: "MER1",
            "venue": "OPS",
            "records": [
                {
                    "channelId": "A-0001",
                    "raw_data": "1.001034,
                    "computed_data": 23.33,
                    "spacecraft_event_time": "2000-01-01T00:00:00",
                    "earth_received_time": "2000-01-03T12:00:00"
                }
            ]
        }
- NOTE: the keys must not have `.`. Example: "channel.id". 
The system expects the following structures in data JSON

        {
            "file / project level metadata": "some values"
            "data grouping name": "array of data in JSON dictionaries of key values. The system supports nested structures, but it is not recommended"
        }
Data JSON should have some of the following properties.

        {
            "(required) one or more of individual measurements such as pressure, temperature, raw_data, computed_data, and so on": "usually a float, but other data types are also supported",
            "(optional) quality flag for each measurement": "usually an integer from 1 to 5. but it can be anything",
            "(required) one or more timestamps such as time, spacecraft_event_time,  earth_received_time": "date-time in string form",
            "(optional) one or more spatial data points such has latitudee, longitude, depth": "usually floats",
        }
2 documents are similar, but the details are different. The system expects a [in_situ_schema.json](in_situ_schema.json) which is a JSON schema which describes what to expects in data JSONs. 

The existing schema can be reused and updated as the system expects the same structure in JSON documents. 

        {
            "type": "object",
            "required": "an array of required file / project level metadata keys AND the data key holding the data array",
            "properties": "a dictionary of file / project level metadata keys and their simple schema. If the schema is complicated, it is referenced back to the 'definitions' key at root level",
            "definitions": "keys and their schemas. If a child schem is repeated, it can be referenced back to this level so that it is not duplicated."
        }
For the other 4 sections, they system expects a [insitu.file.structure.config.json](insitu.file.structure.config.json) which has configurations on data storage structure, and metadata storage configurations.

'insitu.file.structure.config.json' has `data_schema_config` section so that it knows how to read 'in_situ_schema.json'

        {
            "data_array_key": "the name of the key which has the data array. Example: 'data' or 'records' in above examples. 'observations' in original CDMS system.",
            "data_dict_key": "the name of the definition in 'in_situ_schema.json' where data dictionary is defined. Example: 'observation' in original CDMS system. at #/definitions/observation",
            "has_data_quality": "boolean to describe if data has quality values for each data measurements",
            "quality_key_postfix": "if 'has_data_quality' is set to true, quality keys have the same prefix as measurements, but with some postfix to differentiate them. Example: '_quality' in original CDMS system."
        }
### Data Ingestion
'insitu.file.structure.config.json' has `parquet_ingestion_config` section so that it knows how to structure data in Parquet system. 
The system has some predefined data types that is used such as "time", "year", "month", "column", "literal", "insitu_geo_spatial"

        {
            "file_metadata_keys": [  // an array of file / project level metadata keys. Example: mission, spacecraft, venue in spacecaraft engineering system.
                "provider",
                "project"
            ],
            "time_columns": [  // an array of data keys which are timestamps. Example: spacecraft_event_time, earth_received_time in spacecaraft engineering system.
                "time"
            ],           
            "derived_columns": {  // some system columsn are needed for partitioning and to query the data. 
                "time_obj": {  // there should be a '_obj' column for all time keys so that it can be queried by that time column
                    "original_column": "time",  // the original data key from data JSON file
                    "updated_type": "time"  // data type for the new column. For time, it is pyspark "time" datatype. data type needs to be one of the above examples. 
                },
                "year": {  // creating a column for the "year" of the timestamp. This is created as to be used as a partition. It can be removed if partitioning by year is not necessary. 
                    "original_column": "time",
                    "updated_type": "year"
                },
                "month": {  // creating a column for the "month" of the timestamp. This is created as to be used as a partition. It can be removed if partitioning by year is not necessary. 
                    "original_column": "time",
                    "updated_type": "month"
                },
                "platform_code": {  // this is pulling up a nested value of {"platform": {"code": "value"}} so that it is a part of partition. It can be removed if partitioning by it is not necessary
                    "original_column": "platform.code",  // nested dictionary keys are described with '.'. There will be issues if the actual keys also have '.'. 
                    "updated_type": "column"  // since there may be different value for each data row, Spark data type would be the column. 
                },
                "project": {  // this is pulling down a file / project level metadata so that users can query against it. It will be a part of data query. It can also be used for partitions. 
                    "original_column": "project",
                    "updated_type": "literal"  // since the value is fixed for entire data file, it is a literal. 
                },
                "provider": {  // same as 'project'
                    "original_column": "provider",
                    "updated_type": "literal"
                },
                "job_id": {  // this is an external literal value to differentiate each job. 
                    "original_column": "job_id",  // original_column is endpoint parameter key. 
                    "updated_type": "literal"
                },
                "geo_spatial_interval": {  // this is a special column to combine latitude and longitude to form  NxN grids for partitioning. 
                    "original_column": [  // the original_column is an array of 2 which sould be latitude and longitude columns 
                        "latitude",
                        "longitude"
                    ],
                    "split_interval_key": "project",  // the value is the environment key to find which N is used in NxN. More details in https://github.com/wphyojpl/incubator-sdap-in-situ-data-services/pull/3
                    "updated_type": "insitu_geo_spatial"  // special data type only for this system. 
                }
            },
            "partitioning_columns": [  // an array of column names which is used to partition the data in Parquet. A partition is created in the same order. 
                "provider",
                "project",
                "platform_code",
                "geo_spatial_interval",
                "year",
                "month",
                "job_id"
            ],
            "non_data_columns": [  // an array of columns which are not measurements. Do not need to include quality columns here. 
                "time_obj",
                "time",
                "provider",
                "project",
                "platform_code",
                "platform",
                "year",
                "month",
                "job_id",
                "device",
                "latitude",
                "longitude",
                "depth"
            ],
        }
### Metadata Ingestion
'insitu.file.structure.config.json' has `parquet_file_metadata_extraction_config` section so that it knows how to extract statistics from each parquet data block to store them in metadata DB.
The allowed statistics types are "minmax", "data_type_record_count", "record_count".

        [  // It will be an array of configuration what and how to extract required metadata of statistics and data query
            {
                "output_name": "depth",  // dabase column named to store this statistics
                "column": "depth",  // parquet data column to extract the data. 
                "stat_type": "minmax",  // statistics type. minmax will generate 2 outputs min_<output_name> and max_<output_name>
                "min_excluded": -99999.0  // a value to exclude when calculating min max.
                "max_excluded": 99999.0  // a value to exclude when calculating min max.
            },
            {
                "output_name": "lat",  // same as above
                "column": "latitude",
                "stat_type": "minmax"
            },
            {
                "output_name": "lon",  // same as above
                "column": "longitude",
                "stat_type": "minmax"
            },
            {
                "output_name": "datetime",  // same as above
                "column": "time_obj",
                "stat_type": "minmax",
                "special_data_type": "timestamp"  // this is needed when parquet column is not basic data types like string, float, int. 
            },
            {
                "output_name": "observation_counts",  // dabase column named to store this statistics. This name becomes a key to group all measurements / data points statistics
                "stat_type": "data_type_record_count"  // a special type where it will count how many points for each measurement / data points. It will extract data / measurement columns based on #/parquet_ingestion_config/non_data_columns
            },
            {
                "output_name": "total",  // dabase column named to store this statistics
                "stat_type": "record_count"  // statistics type to count how many records in a single Parquet data block
            }
        ]
### Data Statistics Query
'insitu.file.structure.config.json' has `query_statistics_instructions_config` section so that it knows how to query statistics from metadata DB.
- This is created based on Elasticsearch / Opensearch. 

        {
            "group_by": [  // in ES, this is a nested aggregations. Other databases should have similar strategies. 
                        // this config results in grouping each provider. In each provider, group by each project. In each project, group by each platform_code. and so on.
                "provider",
                "project",
                "platform_code"
            ],
            "stats": {  // for each statistics, what types of statistics will be queried? 
                "min": [  // this says query the "min" of the following columns.
                    "min_datetime",
                    "min_depth",
                    "min_lat",
                    "min_lon"
                ],
                "max": [  // this says query the "max" of the following columns. 
                    "max_datetime",
                    "max_depth",
                    "max_lat",
                    "max_lon"
                ],
                "sum": [  // this says make a summation of the values of following columns. 
                    "total"
                ]
            },
            "data_stats": {  // this is a special keys checking if statistics needs to be included for measurements / data points
                "is_included": true,  // boolean to say if it needs to be included. 
                "stats": "sum",  // same as statistics type. 
                "data_prefix": "observation_counts."  // this is to find the prefix of data columns. This needs to match #/parquet_file_metadata_extraction_config/[-2]/output_name
            }
        }
### Data Query
'insitu.file.structure.config.json' has `data_query_config` section so that it knows how to query parquet data. 
- There are several steps to query the data. all the instructions / config in the above dictionary. 
#### Input (Query) Parameters
`data_query_config` section has `input_parameter_transformer_schema` section which describes how to validate incoming parameters. 

        {  // this is a JSON schema to valid incoming key-value pairs.
            "type": "object",
            "properties": {
                "provider": {
                    "type": "string"
                },
                "project": {
                    "type": "string"
                },
                "platform": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "startTime": {
                    "type": "string"
                },
                "endTime": {
                    "type": "string"
                },
                "minDepth": {
                    "type": "number"
                },
                "maxDepth": {
                    "type": "number"
                },
                "bbox": {
                    "type": "array",
                    "items": {
                        "type": "number"
                    }
                },
                "variable": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "columns": {
                    "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
            }
        }
#### Metadata Table Structure
`data_query_config` section has `statics_es_index_schema` section which describes the table / index structure 

        {  // currently this is a Elasticsearch index structure. 
           // this should match some of keys from parquet_file_metadata_extraction_config and query_statistics_instructions_config
            "settings": {
                "number_of_shards": 3,
                "number_of_replicas": 1
            },
            "mappings": {
            "properties": {
                "min_datetime": {
                "type": "double"
                },
                "max_datetime": {
                "type": "double"
                },
                "min_lat": {
                "type": "double"
                },
                "max_lat": {
                "type": "double"
                },
                "min_lon": {
                "type": "double"
                },
                "max_lon": {
                "type": "double"
                },
                "platform_code": {
                "type": "keyword"
                },
                "s3_url": {
                "type": "keyword"
                },
                "bucket": {
                "type": "keyword"
                },
                "geo_spatial_interval": {
                "type": "keyword"
                },
                "month": {
                "type": "keyword"
                },
                "name": {
                "type": "keyword"
                },
                "project": {
                "type": "keyword"
                },
                "provider": {
                "type": "keyword"
                },
                "year": {
                "type": "keyword"
                },
                "total": {
                "type": "long"
                },
                "min_depth": {
                "type": "double"
                },
                "max_depth": {
                "type": "double"
                }
            }
            }
        }
#### Querying metadata in data query
Before querying the actual Parquet data structure, it is helpful to see if there is any relevant data block by querying metadata first. 
`data_query_config` section has `metadata_search_instruction_config` section which describes what to query from metadata. 

        {
            "provider": {  // key name from input parameters. the names need to match. 
                "type": "string",  // datatype of the value that DB is expecting in the query. 
                "dsl_terms": [  // ES DSL query
                {
                    "term": {
                    "provider": "repr_value"  // they key: "provider" needs to match #/data_query_config/statics_es_index_schema
                                              // the value: "repr_value" will be replaced with the actual value. 
                    }
                }
                ]
            },
            "project": {  // same as above
                "type": "string",
                "dsl_terms": [
                {
                    "term": {
                    "project": "repr_value"
                    }
                }
                ]
            },
            "platform": {  // same as above
                "type": "string",
                "dsl_terms": [
                {
                    "term": {
                    "platform_code": "repr_value"
                    }
                }
                ]
            },
            "minDepth": {  // same as above
                "type": "float",
                "dsl_terms": [
                {
                    "range": {  // range DSL instead of term DSL
                    "max_depth": {
                        "gte": "repr_value"
                    }
                    }
                }
                ]
            },
            "maxDepth": {  // same as above
                "type": "float",
                "dsl_terms": [
                {
                    "range": {
                    "min_depth": {
                        "lte": "repr_value"
                    }
                    }
                }
                ]
            },
            "startTime": {  // same as above
                "type": "datetime",  // a special datatype to match the "max_datetime" datatype in 
                                     // #/data_query_config/statics_es_index_schema/properties/max_datetime aka UNIX time
                "dsl_terms": [
                {
                    "range": {
                    "max_datetime": {
                        "gte": "repr_value"
                    }
                    }
                }
                ]
            },
            "endTime": {  // same as above
                "type": "datetime",
                "dsl_terms": [
                {
                    "range": {
                    "min_datetime": {
                        "lte": "repr_value"
                    }
                    }
                }
                ]
            },
            "bbox": [  // input is an array of 4 values. Each of them needs to match each conditions. 
                       // the length of this array needs to match #/data_query_config/input_parameter_transformer_schema/properties/bbox
                {
                "type": "float",
                "dsl_terms": [
                    {
                    "range": {
                        "max_lon": {
                        "gte": "repr_value"
                        }
                    }
                    }
                ]
                },
                {
                "type": "float",
                "dsl_terms": [
                    {
                    "range": {
                        "max_lat": {
                        "gte": "repr_value"
                        }
                    }
                    }
                ]
                },
                {
                "type": "float",
                "dsl_terms": [
                    {
                    "range": {
                        "min_lon": {
                        "lte": "repr_value"
                        }
                    }
                    }
                ]
                },
                {
                "type": "float",
                "dsl_terms": [
                    {
                    "range": {
                        "min_lat": {
                        "lte": "repr_value"
                        }
                    }
                    }
                ]
                }
            ]
        }
#### Querying Parquet for Data
Once the metadata is queried to verify there is data and which section of Parquet has relevant data, those data blocks will be retrieved to perform actual query. 
`data_query_config` section has `parquet_conditions_config` section which describes what to query from metadata. 
- there is a `relationship` keyword how to map input to query term(s).
    - `1:1`: 1 to 1. There is only 1 query term, and the input value is a scalar. 
    - `1:n`: 1 to 1. There are multiple query terms, and the input value is a scalar. 
    - `n:1`: 1 to 1. There is only 1 query term, and the input value is a list. 
        - condition will be repeated for each input values and `condition` key is used to decide how to combine them. 
    - `n:n`: n to n. There are N query terms, and the input value is a list of length n. `condition` key is used to decide how to combine them.
- there is a `condition` key which follows ES DSL `bool` value. Currently it supports `must` and `should` for `AND` and `OR`. 
- there is a `constraint` which defined how the query term is structured. 
    - `binary`: There is a `data_column` which is compare against input value with the `comparator`. 
    - `binary_constant`: This is a special `binary` where  `data_column` is compared against a constant in key `constant` with the `comparator`. 
    - `unary`: There is no `data_column` to compare against the input value. In this case, input value(s) should be the `data_column`s and compared against the `comparator`. 
        - TODO: currently it only supports `includes`. But it should support comparing against a constant. But that might be another `binary_constant`. 
- there is a ES DSL style `comparator` key to use in query terms
    - `gte`: `>=`
    - `lte`: `<=`
    - `eq`: `=`
    - `includes`: `IS NOT NULL`

        {
            "startTime": {  // key name from input parameters. the names need to match. 
                "relationship": "1:1",
                "terms": {
                    "constraint": "binary",
                    "type": "string",
                    "data_column": "time_obj",
                    "comparator": "gte"
                }
            },
            "endTime": {
                "relationship": "1:1",
                "terms": {
                    "constraint": "binary",
                    "type": "string",
                    "data_column": "time_obj",
                    "comparator": "lte"
                }
            },
            "bbox": {
                "relationship": "n:n",
                "condition": "must",
                "terms": [
                    {
                        "constraint": "binary",
                        "type": "float",
                        "data_column": "longitude",
                        "comparator": "gte"
                    },
                    {
                        "constraint": "binary",
                        "type": "float",
                        "data_column": "latitude",
                        "comparator": "gte"
                    },
                    {
                        "constraint": "binary",
                        "type": "float",
                        "data_column": "longitude",
                        "comparator": "lte"
                    },
                    {
                        "constraint": "binary",
                        "type": "float",
                        "data_column": "latitude",
                        "comparator": "lte"
                    }
                ]
            },
            "minDepth": {
                "relationship": "1:n",
                "condition": "should",
                "terms": [
                    {
                        "constraint": "binary",
                        "type": "float",
                        "data_column": "depth",
                        "comparator": "gte"
                    },
                    {
                        "constraint": "binary_constant",
                        "type": "float",
                        "data_column": "depth",
                        "comparator": "eq",
                        "constant": -99999.0
                    }
                ]
            },
            "maxDepth": {
                "relationship": "1:1",
                "terms": {
                    "constraint": "binary",
                    "type": "float",
                    "data_column": "depth",
                    "comparator": "lte"
                }
            },
            "variable": {
                "relationship": "n:1",
                "condition": "should",
                "terms": {
                    "constraint": "unary",
                    "comparator": "includes"
                }
            }
        }