# Project 15 — Deployment Journal

## Objective
Deploy an existing Flask container to Amazon ECS Fargate, expose it for a test, and configure container logging to CloudWatch Logs.

## 1. Networking and security
Previously prepared:
- VPC: `vpc-01c44e7ea49b69463`
- Public subnet: `subnet-04c56a3bb83bc0945` (`10.0.1.0/24`)
- Security group: `sg-01e46e86490958ba6`
- Subnet route to internet gateway was previously confirmed.
- TCP 8000 ingress was configured for public demonstration.

## 2. Image and IAM
- ECR image URI: `881027529328.dkr.ecr.us-east-1.amazonaws.com/project14-webapp:1.0`
- Image digest: `sha256:577447e05391ae29420bb68d531f9561c072b8996040abc12157e3d678cb3ae4`
- Execution role: `ecsTaskExecutionRole`
- `AmazonECSTaskExecutionRolePolicy` was previously verified as attached.

## 3. CloudWatch preparation
- Created log group `/ecs/project15-flask`.
- Task definition configured with the `awslogs` driver.
- Actual log events still need confirmation.

## 4. Task definition
Created local `task-definition.json` and registered it successfully:
- Family `project15-flask`, revision `1`
- Fargate compatibility, `awsvpc` networking
- CPU `256`, memory `512` MiB
- Container `project15-flask`, image tag `project14-webapp:1.0`
- Container port `8000`
- CloudWatch log group `/ecs/project15-flask`
- Region `us-east-1`

## 5. Cluster and service
Created cluster `project15-flask-cluster`, status `ACTIVE`.

Created service `project15-flask-service`:
- Launch type Fargate, desired count 1
- Subnet `subnet-04c56a3bb83bc0945`
- Security group `sg-01e46e86490958ba6`
- Public IP assignment enabled

ECS service output showed `ACTIVE`, desired count 1, running count 1, pending count 0. Service events reported steady state and deployment completion.

## 6. Application test
- Task ID: `3eec7f9336414f568d9c46ae267468fa`
- Task status: `RUNNING`
- Health status: `UNKNOWN` (no health-check result shown)
- Network interface: `eni-0d600a09ba136656b`
- Public IP observed: `18.206.87.153`
- User confirmed `http://18.206.87.153:8000` was reachable in a browser.

## Result
**ECS/Fargate deployment and public browser reachability are confirmed.**

## Remaining tasks
- Capture portfolio screenshots listed in README.
- Confirm actual CloudWatch log streams/events.
- Restrict inbound TCP 8000 after public demo is no longer needed.
- Avoid root credentials for routine AWS CLI work.
- Review potential AWS charges and clean up lab resources when appropriate.

## Learning reflection
The task definition is the container blueprint; the ECS service maintains desired task count; Fargate supplies managed compute; the task ENI and security group govern connectivity; CloudWatch Logs receives output when configured and functioning.
