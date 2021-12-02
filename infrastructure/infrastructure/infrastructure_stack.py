from aws_cdk import aws_apigatewayv2 as apigateway
from aws_cdk import aws_apigatewayv2_integrations as _apigw_integration
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_secretsmanager as secretsmanager
from aws_cdk import aws_lambda_python as _lambda_python
from aws_cdk import core


class InfrastructureStack(core.Stack):
    def __init__(
        self, scope: core.Construct, construct_id: str, *, app_name: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # TODO: Add vpc_config, custom domain & envs to the stack

        dynamo_auth_user = dynamodb.Table(
            self,
            id=f'{app_name}-Dynamo',
            table_name='AuthUserTable',
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            partition_key=dynamodb.Attribute(
                name='userId', type=dynamodb.AttributeType.STRING
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        secrets = secretsmanager.Secret.from_secret_name_v2(
            self, "AuthUserSecrets", secret_name='test_auth_secrets'
        )

        lambda_fastapi = _lambda_python.PythonFunction(
            self,
            id=f'{app_name}-app',
            entry='../code',
            index='main.py',
            handler='handler',
            runtime=lambda_.Runtime.PYTHON_3_8,
            environment=dict(  # TODO: Add env vars to the stack. Should use the same from .env in code
                UserTable=dynamo_auth_user.table_name,
                DEBUG='1',
                PROJECT_NAME='auth-service',
                BACKEND_CORS_ORIGINS='["http://localhost:8000", "https://localhost:8000", "https://6dzwaufot8.execute-api.us-west-2.amazonaws.com/"]',
                DB_KEY=secrets.secret_value_from_json("AWS_KEY").to_string()
                ),
            timeout=core.Duration.seconds(60),  # TODO: check the timeout
        )

        # grant permission to lambda to read from table
        dynamo_auth_user.grant_read_data(lambda_fastapi)
        # grant permission to lambda to write to table
        dynamo_auth_user.grant_write_data(lambda_fastapi)

        base_api = apigateway.HttpApi(
            self,
            id=f'{app_name}-api',
            api_name=f'{app_name}-apigateway',
            default_integration=_apigw_integration.LambdaProxyIntegration(
                handler=lambda_fastapi
            ),
        )

        core.CfnOutput(
            self,
            id=f'{app_name}-endpoint',
            value=base_api.api_endpoint,
            export_name=f'{app_name}-url',
        )
