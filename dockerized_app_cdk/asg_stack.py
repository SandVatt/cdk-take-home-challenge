from unicodedata import name
from aws_cdk.aws_ec2 import SubnetType

from aws_cdk import (
    Tag,
    aws_ec2 as ec2,
     aws_iam as iam,
    aws_autoscaling as autoscaling,
    aws_elasticloadbalancingv2 as elbv2,
    Stack
    )

from constructs import Construct

class ASGStack(Stack):

    def __init__(self, scope: Construct, id: str, props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        userdata_file = open("./userdata.sh", "rb").read()
        # Creates a userdata object for Linux hosts
        userdata = ec2.UserData.for_linux()
        # Adds one or more commands to the userdata object.
        userdata.add_commands(str(userdata_file, 'utf-8'))
        role = iam.Role(self, "Instance-ec2-role", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryFullAccess"))

        asg = autoscaling.AutoScalingGroup(
            self,
            "app-asg",
            vpc=props['vpc'],
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.MEMORY5, ec2.InstanceSize.XLARGE
            ),
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
                ),
            key_name="key-1",
            vpc_subnets=ec2.SubnetSelection(subnet_type=SubnetType.PRIVATE_WITH_NAT),
            user_data=userdata,
            desired_capacity=1,
            min_capacity=1,
            max_capacity=1,
            role=role
        )

        # Creates a security group for application
        sg_nginx = ec2.SecurityGroup(
                self,
                id="sg_nginx",
                vpc=props['vpc'],
                security_group_name="sg_nginx"
        )

        # Allows only the IP of "123.123.123.123"
        # to access this security group for SSH
        sg_nginx.add_ingress_rule(
            peer=ec2.Peer.ipv4("151.66.226.30/32"),
            connection=ec2.Port.tcp(22)
        )

        # Creates a security group for the application load balancer
        sg_alb = ec2.SecurityGroup(
                self,
                id="sg_alb",
                vpc=props['vpc'],
                security_group_name="sg_alb"
        )

        # Allows connections from security group "sg_alb"
        # inside the "sg_nginx" security group to access port 8080
        # where our app listens
        sg_nginx.connections.allow_from(
                sg_alb, ec2.Port.tcp(8080), "Ingress")

        # Adds the security group 'sg_nginx' to the autoscaling group
        asg.add_security_group(sg_nginx)

        # Creates an application load balance
        lb = elbv2.ApplicationLoadBalancer(
                self,
                "ALB",
                vpc=props['vpc'],
                security_group=sg_alb,
                internet_facing=True)

        listener = lb.add_listener("Listener", port=80)
        # Adds the autoscaling group's (asg) instance to be registered
        # as targets on port 8080
        listener.add_targets("Target", port=8080, targets=[asg])
        # This creates a "0.0.0.0/0" rule to allow every one to access the
        # application
        listener.connections.allow_default_port_from_any_ipv4(
                "Open to the world"
                )