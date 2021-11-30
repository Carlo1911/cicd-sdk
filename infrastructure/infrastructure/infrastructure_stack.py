from aws_cdk import aws_apigatewayv2 as apigateway
from aws_cdk import aws_apigatewayv2_integrations as _apigw_integration
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_lambda as lambda_
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

        lambda_fastapi = _lambda_python.PythonFunction(
            self,
            id=f'{app_name}-app',
            entry='../code',
            index='code/app/main.py',
            handler='handler',
            runtime=lambda_.Runtime.PYTHON_3_8,
            environment=dict(UserTable=dynamo_auth_user.table_name, DEBUG='1'),
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
