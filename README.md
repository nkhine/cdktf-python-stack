# cdktf-python-stack

This project has a single flask application running in a Docker container and has an infrastructure composed using AWS-CDKTF

Currently the app is working and we have 3 AWS Resources being created:
* VPC
* ECS
* ECS Task

There are some helper scripts to help you setup your local environment.

Please ensure to update the `infra/provisiong.sh` script and set the:
* AWS_PROFILE
* S3_BUCKET_NAME

IMPORTANT: `S3_BUCKET_NAME` - needs to be created before you deploy the stack as this is used by Terraform.

There is no CICD in place, although, I have added some Dockerfile which can be used in Jenkins or other CI, please note these are not fully tested.

We could create a CodePipeline within the stack and use this to deploy to the environment, using a self mutating pipeline.

Unfinnished work:
- Setting up the ECR repository
- Build pipelines
- CICD
- Tests - both for the app and infra
- ECS Task to use the app image
- VPC - security (ingress) permissions.