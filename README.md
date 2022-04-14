# Dockerized App and AWS CDK Python project

This is a project to deploy a dockerized application on AWS with the AWS Cloud Development Kit.

This project also demonstrates using a multi-stack approach to create a networking layer, autoscaling group with a load balancer.
It also deploys the containerized application in the private subnet with a load balancer and NAT gateway in the public subnet.
It also demonstrates how to allow other security groups as an ingress source to other security groups.
Furthermore, an example of how to load userdata into the autoscaling group is also shown.


NetworkStack - creates subnets, VPCs and routes and route tables
ASGStack - contains the code for an autoscaling group, application loadbalancer
and some security groups to allow the load balancer to access the instance.  Also
contains an example on how to load user data into the instance.


## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
