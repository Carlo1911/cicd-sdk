#!/usr/bin/env python3
import os
import aws_cdk as cdk

from infrastructure.infrastructure_stack import AuthUserServiceStack
from infrastructure.config import get_config

env_name = os.environ.get('ENV_NAME', 'Prod')

app = cdk.App()
config = get_config(deploy_name=env_name)
AuthUserServiceStack(app, f"{env_name}AuthUserService", app_name=f"{env_name}AuthUserService", config=config)

app.synth()
