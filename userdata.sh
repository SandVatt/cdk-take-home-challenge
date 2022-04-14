#!/bin/sh

yum install docker -y
yum install -y amazon-efs-utils
yum install jq -y


# enable and start docker
systemctl enable docker
systemctl start docker

# Adding EC2 user to docker user group 
usermod -aG docker ec2-user
# Authenticating to ECR to pull the image and get the image tag

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws_accid>.dkr.ecr.us-east-1.amazonaws.com
# Getting the image tag from ECR
export image_tag=$(aws ecr describe-images --repository-name <repo_name> --region us-east-1 | jq -r .imageDetails[].'imageTags[]')


docker run --name mynginx -p 8080:8080 -d <aws_accid>.dkr.ecr.us-east-1.amazonaws.com/cdk-hnb659fds-container-assets-177664371233-us-east-1:$image_tag


