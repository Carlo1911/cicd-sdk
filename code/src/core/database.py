import os

import boto3
from src.core.config import settings


if os.environ.get("IS_OFFLINE"):
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=f"http://{os.environ.get('HOSTNAME')}:4566/",
        region_name=settings.REGION,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
        use_ssl=False,
        verify=False,
    )
else:
    dynamodb = boto3.resource("dynamodb")
