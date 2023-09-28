/*
Licensed to the Apache Software Foundation (ASF) under one or more
contributor license agreements.  See the NOTICE file distributed with
this work for additional information regarding copyright ownership.
The ASF licenses this file to You under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with
the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}

locals {
  resource_prefix = "${var.project}-${var.environment}"
  account_id = data.aws_caller_identity.current.account_id
  lambda_file_name = "${path.module}/build/cdms_lambda_functions.zip"
  security_group_ids_set = var.security_group_ids != null
}

resource "aws_security_group" "insitu_lambda_sg" {
  count  = local.security_group_ids_set ? 0 : 1
  vpc_id = var.insitu_lambda_vpc_id
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = var.tags
}