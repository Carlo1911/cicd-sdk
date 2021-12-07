from aws_cdk.aws_apigatewayv2_alpha import HttpApi
from aws_cdk.aws_apigatewayv2_integrations_alpha import LambdaProxyIntegration
from aws_cdk.aws_dynamodb import  Attribute, AttributeType, BillingMode, Table
from aws_cdk.aws_lambda import Runtime
from aws_cdk.aws_secretsmanager import  Secret
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from aws_cdk import CfnOutput, Duration, RemovalPolicy, Stack
from constructs import Construct



class InfrastructureStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, *, app_name: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # TODO: Add vpc_config, custom domain & envs to the stack

        dynamo_auth_user = Table.from_table_name(
            self,
            id=f'{app_name}-Dynamo',
            table_name='AuthUserTable',
            # partition_key=Attribute(
            #     name="user_id", type=AttributeType.STRING,
            # ),
            # billing_mode=BillingMode.PAY_PER_REQUEST,
        )

        if not dynamo_auth_user.table_name:

            dynamo_auth_user = Table(
                self,
                id=f'{app_name}-Dynamo',
                table_name='AuthUserTable',
                billing_mode=BillingMode.PAY_PER_REQUEST,
                partition_key=Attribute(
                    name='userId', type=AttributeType.STRING
                ),
                removal_policy=RemovalPolicy.RETAIN,
            )

        # secrets = secretsmanager.Secret.from_secret_name_v2(
        #     self, "AuthUserSecrets", secret_name='Auth-User-Service-Secrets'
        # )

        lambda_fastapi = PythonFunction(
            self,
            id=f'{app_name}-app',
            entry='../code',
            index='main.py',
            handler='handler',
            runtime=Runtime.PYTHON_3_8,
            environment=dict(
                PROJECT_NAME='auth-service',
                BACKEND_CORS_ORIGINS='["https://6dzwaufot8.execute-api.us-west-2.amazonaws.com/"]',
                DB_TABLE=dynamo_auth_user.table_name,
                # TODO: Add AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and AWS_REGION
                # DB_AWS_KEY=secrets.secret_value_from_json("AWS_KEY").to_string(),
                # DB_AWS_SECRET=secrets.secret_value_from_json("AWS_SECRETS").to_string(),
                ),
            timeout=Duration.seconds(5),  # TODO: check the timeout
        )

        # grant permission to lambda to read and write from table
        dynamo_auth_user.grant_read_write_data(lambda_fastapi)

        base_api = HttpApi(
            self,
            id=f'{app_name}-api',
            api_name=f'{app_name}-apigateway',
            default_integration=LambdaProxyIntegration(
                handler=lambda_fastapi
            ),
        )

        CfnOutput(
            self,
            id=f'{app_name}-endpoint',
            value=base_api.api_endpoint,
            export_name=f'{app_name}-url',
        )
