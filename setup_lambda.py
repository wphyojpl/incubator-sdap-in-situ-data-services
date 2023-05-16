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

from setuptools import find_packages, setup


install_requires = [
    'attrs==22.1.0',
    'boto3==1.24.74',
    'botocore==1.27.74',
    'certifi==2022.9.14',
    'charset-normalizer==2.0.12',
    'elasticsearch==7.13.4',
    'fastjsonschema==2.15.1',
    'idna==3.4',
    'importlib-metadata==4.12.0',
    'importlib-resources==5.9.0',
    'jmespath==1.0.1',
    'jsonschema==4.16.0',
    'pkgutil_resolve_name==1.3.10',
    'py4j==0.10.9',
    'pyrsistent==0.18.1',
    'pyspark==3.1.2',
    'python-dateutil==2.8.2',
    'requests==2.26.0',
    'requests-aws4auth==1.1.1',
    's3transfer==0.6.0',
    'six==1.16.0',
    'typing_extensions==4.3.0',
    'urllib3==1.26.12',
    'zipp==3.8.1'
]

setup(
    name="parquet_ingestion_search",
    version="0.0.1",
    packages=find_packages(),
    install_requires=install_requires,
    author="Apache SDAP",
    author_email="dev@sdap.apache.org",
    python_requires="==3.7",
    license='NONE',
    include_package_data=True,
)
