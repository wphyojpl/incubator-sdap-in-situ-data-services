import os



os.environ['master_spark_url'] = ''
os.environ['spark_app_name'] = ''
os.environ['parquet_file_name'] = ''
os.environ['aws_access_key_id'] = 'AKIA4LBYFVFVZ5RD6F7O'
os.environ['aws_secret_access_key'] = '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'
os.environ['aws_session_token'] = ''
os.environ['in_situ_schema'] = ''
os.environ['authentication_type'] = ''
os.environ['authentication_key'] = ''
os.environ['parquet_metadata_tbl'] = ''


from parquet_flask.aws.es_abstract import ESAbstract
from parquet_flask.aws.es_factory import ESFactory

index = 'test1'
es_url = 'https://search-insitu-parquet-dev-1-vgwt2bx23o5w3gpnq4afftmvaq.us-west-2.es.amazonaws.com/'
aws_es: ESAbstract = ESFactory().get_instance('AWS', index=index, base_url=es_url, port=443)

print(aws_es.query({'query': {'match_all': {}}}))
