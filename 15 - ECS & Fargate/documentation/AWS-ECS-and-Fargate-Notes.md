# Project 15 — Technical Notes

## Component roles
- **ECR:** stores the container image.
- **ECS:** orchestrates tasks and services.
- **Fargate:** provides managed container compute without user-managed EC2 hosts.
- **Task definition:** blueprint for image, resources, networking, port mappings, execution role, and logging.
- **ECS service:** maintains the requested task count; this service requests one task.
- **VPC/subnet:** network placement for the task's elastic network interface.
- **Security group:** stateful firewall controlling traffic.
- **Public IP:** allows internet connectivity subject to routing and security rules.
- **CloudWatch Logs:** receives container output when the logging driver and permissions are working.

## Task-definition settings
- `family: project15-flask`: groups task-definition revisions.
- `networkMode: awsvpc`: each task receives its own network interface.
- `requiresCompatibilities: ["FARGATE"]`: declares Fargate compatibility.
- `cpu: "256"`: 0.25 vCPU.
- `memory: "512"`: 512 MiB.
- `executionRoleArn`: role used by ECS/Fargate to pull the image and initialize logging. This differs from a task role used by application code to call AWS services.
- `containerPort: 8000`: must match the port on which Flask listens.
- `awslogs`: configured to send container output to `/ecs/project15-flask` in `us-east-1`, stream prefix `ecs`.

## Confirmed resource identifiers
- Account: `881027529328`
- Region: `us-east-1`
- ECR image: `881027529328.dkr.ecr.us-east-1.amazonaws.com/project14-webapp:1.0`
- Image digest: `sha256:577447e05391ae29420bb68d531f9561c072b8996040abc12157e3d678cb3ae4`
- Cluster: `project15-flask-cluster`
- Service: `project15-flask-service`
- Task definition: `project15-flask:1`
- Task ID: `3eec7f9336414f568d9c46ae267468fa`
- ENI: `eni-0d600a09ba136656b`
- Public IP observed: `18.206.87.153`
- VPC: `vpc-01c44e7ea49b69463`
- Subnet: `subnet-04c56a3bb83bc0945`, CIDR `10.0.1.0/24`
- Security group: `sg-01e46e86490958ba6`
- Log group: `/ecs/project15-flask`
- Execution role: `ecsTaskExecutionRole`

## Observed state
- ECS service status `ACTIVE`; desired 1, running 1, pending 0.
- Service events reported steady state and deployment completion.
- Task status `RUNNING`; health status `UNKNOWN`.
- User confirmed the public endpoint `http://18.206.87.153:8000` was reachable.
- Log group creation is confirmed, but actual log events still need checking.
- Public IP can change if ECS replaces the task.
- Security group allows TCP 8000 from `0.0.0.0/0` for the demo; restrict after testing.
- AWS CLI was using root credentials. Use an appropriately permissioned IAM identity for routine work.

## Troubleshooting
1. Browser timeout: inspect ingress, public IP, route to internet gateway, and whether Flask binds to `0.0.0.0:8000`.
2. Task stops: inspect ECS service events and stopped reason; then inspect logs.
3. No log stream: check stdout/stderr output, task execution role, and `awslogs` configuration.
4. Port mismatch: update task definition and service to use the app's actual listening port.
5. New task IP: retrieve the replacement task's ENI and associated public IP.

## Interview summary
“I packaged a Flask app as a container image and stored it in Amazon ECR. I registered an ECS task definition for Fargate with CPU/memory, port mapping, an execution role, and CloudWatch logging. I deployed it through an ECS service in my VPC, verified that ECS reached steady state with one running task, and confirmed browser access through the task's public IP on port 8000.”

Do not claim autoscaling, high availability, HTTPS, load balancing, CI/CD, or confirmed log ingestion unless separately implemented and verified.
