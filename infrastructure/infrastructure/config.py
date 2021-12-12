import os
from dataclasses import dataclass

from aws_cdk import RemovalPolicy


@dataclass(frozen=True)
class Config:
    """
    Auth User Service CDK deployment config

    Default values are good for non-production environments
    """

    project_name: str = "Auth user service"
    db_table_name: str = "AuthUserTable"
    db_removal_policy: RemovalPolicy = RemovalPolicy.DESTROY
    region: str = "us-west-2"
    backend_cors_origin: str = os.environ.get(
        "ENDPOINT_CORS_ORIGIN", "['http://localhost:9001/']"
    )


def get_config(*, deploy_name: str) -> Config:
    if deploy_name == "Prod":
        return Config(
            db_removal_policy=RemovalPolicy.RETAIN,
        )
    return Config()
