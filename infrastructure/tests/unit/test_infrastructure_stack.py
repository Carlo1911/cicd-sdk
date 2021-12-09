import aws_cdk as core
import aws_cdk.assertions as assertions

from infrastructure.infrastructure_stack import AuthUserServiceStack


def test_sqs_queue_created():
    app = core.App()
    stack = AuthUserServiceStack(app, "ProdAuthUserService", app_name="ProdAuthUserService")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SQS::Queue", {"VisibilityTimeout": 300})
