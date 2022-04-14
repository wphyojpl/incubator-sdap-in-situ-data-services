import os

from parquet_flask.__main__ import flask_me

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

flask_me()
