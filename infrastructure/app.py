#!/usr/bin/env python3
import aws_cdk as cdk

from infrastructure.infrastructure_stack import InfrastructureStack

app = cdk.App()
InfrastructureStack(app, "ProdAuthUserService", app_name="ProdAuthUserService")

app.synth()
