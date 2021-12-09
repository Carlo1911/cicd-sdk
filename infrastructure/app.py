#!/usr/bin/env python3
import aws_cdk as cdk

from infrastructure.infrastructure_stack import AuthUserServiceStack

app = cdk.App()
AuthUserServiceStack(app, "ProdAuthUserService", app_name="ProdAuthUserService")

app.synth()
