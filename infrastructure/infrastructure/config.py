from dataclasses import dataclass
from aws_cdk import RemovalPolicy


@dataclass(frozen=True)
class Config:
    """
    Auth User Service CDK deployment config

    Default values are good for non-production environments
    """

    termination_protection: bool
    project_name: str = "Auth user service"
    db_table_name: str = "AuthUserTable"
    db_removal_policy: RemovalPolicy = RemovalPolicy.DESTROY


def get_config(*, deploy_name: str) -> Config:
    if deploy_name == "Prod":
        return Config(
            termination_protection=True,
            db_removal_policy=RemovalPolicy.RETAIN,

        )
    return Config(
        termination_protection=False,
    )
