import os

import boto3


if os.environ.get("IS_OFFLINE"):
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=f"http://{os.environ.get('HOSTNAME')}:4566/",
    )
else:
    dynamodb = boto3.resource("dynamodb")
