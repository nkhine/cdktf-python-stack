#!/usr/bin/env python
from cdktf import App
from stacks.networking_stack import NetworkingStack, NetworkingStackConfig

TAG_NAME_PREFIX = "phrasee-stack-"
app = App()

networking_stack = NetworkingStack(
    app,
    "NetworkingStack",
    NetworkingStackConfig(
        tag_name_prefix=TAG_NAME_PREFIX,
    ),
)

app.synth()
