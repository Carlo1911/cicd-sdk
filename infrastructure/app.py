#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infrastructure.config import get_config
from infrastructure.infrastructure_stack import AuthUserServiceStack

env_name = os.environ.get("ENV_NAME", "Prod")
app_name = f"{env_name}AuthUserService"

app = cdk.App()
config = get_config(deploy_name=env_name)
AuthUserServiceStack(app, app_name, app_name=app_name, config=config)

app.synth()
