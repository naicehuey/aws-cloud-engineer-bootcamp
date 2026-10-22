# Project 15 — Learning Notes

## Component roles
- **ECR:** stores the image.
- **ECS:** runs and manages tasks and services.
- **Fargate:** managed compute, no EC2 hosts for me to run.
- **Task definition:** blueprint (image, size, port, role, logging).
- **Service:** keeps the wanted number of tasks running (1 here).
- **Cluster:** groups services and tasks.
- **VPC and subnet:** where the task's network interface lives.
- **Security group:** stateful firewall.
- **CloudWatch Logs:** receives container output when logging works.

## Task definition settings (`project/task-definition.json`)
- `family: project15-flask`: groups revisions
- `networkMode: awsvpc`: one network interface per task
- `requiresCompatibilities: ["FARGATE"]`
- `cpu: "256"` is 0.25 vCPU, `memory: "512"` is 512 MiB
- `executionRoleArn`: used by ECS to pull the image and set up logs (not for app code)
- `containerPort: 8000`: must match Flask's port
- `awslogs`: sends output to `/ecs/project15-flask`, stream prefix `ecs`

## Flow
```text
Register task definition -> create cluster -> create service (desired 1)
-> Fargate starts the task -> pulls image from ECR -> task gets a public IP
-> browser opens http://<public IP>:8000
```

## What I observed
- Service ACTIVE, desired 1, running 1, pending 0
- Service events: steady state
- Task RUNNING, health UNKNOWN (no health check configured)
- App reachable in the browser on port 8000
- Log group created. Log events not confirmed yet.

## Execution role vs task role
- **Execution role:** for ECS itself (pull image, send logs).
- **Task role:** for the app's own calls to AWS services. Not used here.

## Troubleshooting
```text
Browser timeout     -> security group 8000? public IP on? route to internet gateway? Flask on 0.0.0.0:8000?
Task keeps stopping -> service events, stopped reason, then logs
No log stream       -> does the app write to stdout? execution role? awslogs settings?
Port mismatch       -> fix the task definition, register a new revision, update the service
New IP              -> find the new task's network interface and public IP
```

## Security
- Port 8000 is open to `0.0.0.0/0` for the demo. Restrict or remove it.
- Don't use root credentials for the CLI. Use an IAM user or role with limited permissions.

## What I can and can't claim
Can: containerised Flask app on ECS Fargate, running as a service in my VPC, reachable by public IP.
Can't (not built): load balancer, HTTPS, autoscaling, CI/CD, confirmed log ingestion.

## Cost awareness
Set desired count to 0, delete the service and cluster, remove the log group if not needed, check Billing.

## Self-test
1. What is a task definition?
2. What does an ECS service do?
3. What is Fargate?
4. Execution role or task role?
5. Why must `containerPort` match the app?
6. Why can the public IP change?
7. What does `awsvpc` do?

### Answers
1. The blueprint for a container: image, size, port, role and logging.
2. It keeps the requested number of tasks running.
3. Managed compute for containers, with no servers for me to manage.
4. The execution role lets ECS pull the image and send logs. A task role is for the app's own AWS calls.
5. If it doesn't match the port Flask listens on, the traffic doesn't reach the app.
6. A replacement task gets a new network interface and address.
7. Each task gets its own network interface in my subnet.

## One-sentence memory rule
> **ECR stores the image, the task definition describes it, the service keeps it running, and Fargate supplies the compute.**
