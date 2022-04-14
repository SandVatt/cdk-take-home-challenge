from aws_cdk import (
    aws_rds as rds,
    aws_ec2 as ec2,
    RemovalPolicy, Stack
    )
from constructs import Construct
from aws_cdk import CfnOutput
from aws_cdk.aws_ecr_assets import DockerImageAsset
from os import path
import os 
import subprocess

class DockerStack(Stack):
    def __init__(self, scope: Construct, id: str, props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # Create an Image and push to ECR
        asset = DockerImageAsset(self, "nginx-image",
        directory=path.join("my-image")
        )



    @property
    def outputs(self):
        return self.output_props