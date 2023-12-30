#!/usr/bin/env python
from cdktf import App
from stacks.networking_stack import NetworkingStack, NetworkingStackConfig
from stacks.ecs_stack import EcsStack, EcsStackConfig

TAG_NAME_PREFIX = "phrasee-stack-"
app = App()

networking_stack = NetworkingStack(
    app,
    "NetworkingStack",
    NetworkingStackConfig(
        tag_name_prefix=TAG_NAME_PREFIX,
    ),
)
ecs_stack = EcsStack(
    app,
    "EcsStack",
    EcsStackConfig(
        region=networking_stack.region,
        aws_vpc=networking_stack.aws_vpc,  # Pass the VPC reference
        internet_gateway=networking_stack.aws_internet_gateway,  # Pass the Internet Gateway reference
        aws_public_subnet=networking_stack.aws_public_subnet,
    ),
    # dependencies=[networking_stack],  # Make ECS stack dependent on Networking stack
)
app.synth()
