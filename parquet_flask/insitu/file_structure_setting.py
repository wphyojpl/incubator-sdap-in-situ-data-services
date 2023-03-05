from parquet_flask.utils.parallel_json_validator import ParallelJsonValidator

STRUCTURE_CONFIG = {
    "type": "object",
    "required": ["partitioning_columns", "non_data_columns", "derived_columns", "file_metadata_keys", "data_array_key", "data_stats", "query_input_metadata_search_instructions", "query_input_transformer_schema"],
    "properties": {
        "data_array_key": {"type": "string"},
        "partitioning_columns": {"type": "array", "items": {"type": "string"}},
        "non_data_columns": {"type": "array", "items": {"type": "string"}},
        "metadata_keys": {"type": "array", "items": {"type": "string"}},
        "derived_columns": {
            "type": "object",
            "required": [],
            "properties": {}
        },
        "query_input_transformer_schema": {"type": "object"},
        "query_input_metadata_search_instructions": {
            "type": "object"
        },
        "data_stats": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["stat_type", "output_name"],
                "properties": {
                    "output_name": {"type": "string"},
                    "stat_type": {
                        "type": "string",
                        "enum": ["minmax", "count", "record_count"]
                    },
                    "special_data_type": {
                        "type": "string",
                        "enum": ["timestamp"]
                    },
                    "column": {"type": "string"},
                    "columns": {"type": "array", "items": {"type": "string"}}
                }
            }
        }
    }
}


class FileStructureSetting:
    def __init__(self, data_json_schema: dict, structure_config: dict):
        self.__data_json_schema = data_json_schema
        self.__structure_config = structure_config
        result, message = ParallelJsonValidator().load_schema(STRUCTURE_CONFIG).validate_single_json(self.__structure_config)
        if result is False:
            raise ValueError(f'invalid structure_config: {message}')

    def get_query_input_transformer_schema(self):
        return self.__structure_config['query_input_transformer_schema']
    def query_input_metadata_search_instructions(self):
        return self.__structure_config['query_input_metadata_search_instructions']

    def get_file_metadata_keys(self):
        return self.__structure_config['file_metadata_keys']

    def get_data_array_key(self):
        return self.__structure_config['data_array_key']

    def get_derived_columns(self):
        return self.__structure_config['derived_columns']

    def get_data_stats_config(self):
        return self.__structure_config['data_stats']

    def get_partitioning_columns(self):
        return self.__structure_config['partitioning_columns']
