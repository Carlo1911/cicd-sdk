#!/usr/bin/env python3

import aws_cdk as cdk
from infrastructure.infrastructure_stack import InfrastructureStack

app = cdk.App()
InfrastructureStack(app, 'stage-user-service', app_name='stage-AuthUserService')

app.synth()
