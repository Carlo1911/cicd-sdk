from aws_cdk import CfnOutput
from aws_cdk import Duration
from aws_cdk import Stack
from aws_cdk.aws_apigatewayv2_alpha import HttpApi
from aws_cdk.aws_apigatewayv2_integrations_alpha import LambdaProxyIntegration
from aws_cdk.aws_dynamodb import Attribute
from aws_cdk.aws_dynamodb import AttributeType
from aws_cdk.aws_dynamodb import BillingMode
from aws_cdk.aws_dynamodb import Table
from aws_cdk.aws_lambda import Runtime
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from constructs import Construct

from .config import Config


class AuthUserServiceStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        app_name: str,
        config=Config,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # TODO: Add vpc_config, custom domain and backups

        dynamo_auth_user = Table(
            self,
            id=f"{app_name}-Dynamo",
            table_name=config.db_table_name,
            billing_mode=BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery=True,
            partition_key=Attribute(name="uid", type=AttributeType.STRING),
            removal_policy=config.db_removal_policy,
        )

        lambda_fastapi = PythonFunction(
            self,
            id=f"{app_name}-app",
            entry="../code",
            index="main.py",
            handler="handler",
            runtime=Runtime.PYTHON_3_9,
            environment=dict(
                PROJECT_NAME=config.project_name,
                BACKEND_CORS_ORIGINS=config.backend_cors_origin,
                DB_TABLE=config.db_table_name,
                REGION=config.region,
            ),
            timeout=Duration.seconds(5),
        )

        # grant permission to lambda to read and write from table
        dynamo_auth_user.grant_read_write_data(lambda_fastapi)

        base_api = HttpApi(
            self,
            id=f"{app_name}-api",
            api_name=f"{app_name}-apigateway",
            default_integration=LambdaProxyIntegration(handler=lambda_fastapi),
        )

        CfnOutput(
            self,
            id=f"{app_name}-endpoint",
            value=base_api.api_endpoint,
            export_name=f"{app_name}-url",
        )
