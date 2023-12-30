#!/usr/bin/env python

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from constructs import Construct
from cdktf import TerraformStack, S3Backend
from imports.aws.provider import AwsProvider


S3_BUCKET_NAME = "phrasee-cdktf"


class BaseStack(TerraformStack):
    def __init__(self, scope: Construct, id: str, region: str):
        super().__init__(scope, id)

        AwsProvider(self, "AWS", region=region, profile="aqoon")

        S3Backend(self, bucket=S3_BUCKET_NAME, key=f"{id}TerraformState", region=region)
