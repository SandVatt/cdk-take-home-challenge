#!/usr/bin/env python3

from aws_cdk import App

from dockerized_app_cdk.network_stack import NetworkStack
from dockerized_app_cdk.docker_stack import DockerStack
from dockerized_app_cdk.asg_stack import ASGStack


props = {'namespace': 'NetworkStack '}
app = App()
ns = NetworkStack(app, "NetworkStack", props)

docker = DockerStack(app, "DockerStack", ns.outputs)
# rds.add_dependency(ns)

asg = ASGStack(app, "ASGStack", ns.outputs)
asg.add_dependency(ns)
asg.add_dependency(docker)


app.synth()