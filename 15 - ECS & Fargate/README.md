# Project 15 — Flask on Amazon ECS Fargate

## Overview
Deploy an existing containerized Flask app to Amazon ECS using AWS Fargate. The image is stored in ECR, the task runs in a VPC subnet with a public IP, and container logging is configured for CloudWatch Logs.

## Confirmed configuration
| Item | Value |
|---|---|
| Account | `881027529328` |
| Region | `us-east-1` |
| ECR image | `881027529328.dkr.ecr.us-east-1.amazonaws.com/project14-webapp:1.0` |
| ECS cluster | `project15-flask-cluster` |
| ECS service | `project15-flask-service` |
| Task definition | `project15-flask:1` |
| Launch type | Fargate |
| CPU / memory | `256` CPU units / `512` MiB |
| Container port | `8000` |
| Execution role | `ecsTaskExecutionRole` |
| CloudWatch log group | `/ecs/project15-flask` |
| VPC | `vpc-01c44e7ea49b69463` |
| Subnet | `subnet-04c56a3bb83bc0945` (`10.0.1.0/24`) |
| Security group | `sg-01e46e86490958ba6` |
| Task ENI | `eni-0d600a09ba136656b` |
| Public IP observed | `18.206.87.153` |

**The public IP may change if ECS replaces the task.** Treat it as the observed address during this test, not a permanent endpoint.

## What was done
1. Prepared the VPC, subnet, internet-gateway route, and security group.
2. Used the existing ECR image `project14-webapp:1.0`.
3. Prepared `ecsTaskExecutionRole` with `AmazonECSTaskExecutionRolePolicy`.
4. Created CloudWatch log group `/ecs/project15-flask`.
5. Created `task-definition.json` for Fargate, `awsvpc`, 256 CPU units, 512 MiB memory, port 8000, and `awslogs`.
6. Registered task definition revision 1.
7. Created cluster `project15-flask-cluster`.
8. Created service `project15-flask-service`, desired count 1, using the existing subnet/security group with public IP assignment enabled.
9. ECS reported the service reached steady state with 1 running task.
10. Retrieved public IP `18.206.87.153`; user confirmed the app was reachable in a browser.

## Architecture
See [`architecture/architecture-diagram.md`](architecture/architecture-diagram.md).

## Screenshot evidence
Save actual screenshots in `screenshots/`:
- `01-live-flask-application.png` — browser showing the real app and address bar.
- `02-ecs-service-running.png` — service showing desired 1 / running 1.
- `03-ecs-task-definition.png` — revision 1 JSON or container details showing image, port, role, logs, CPU, and memory.
- `04-fargate-task-networking.png` — task networking, subnet, security group, ENI, and public IP if shown.
- `05-cloudwatch-container-logs.png` — actual log stream/events. Do not claim logs exist until events are visible.
- `06-ecr-container-image.png` — repository image tag 1.0 and digest (supporting evidence).

## Security and cost notes
- The security group was described as allowing inbound TCP 8000 from `0.0.0.0/0`; this exposes the demonstration app publicly. Restrict or remove this rule when public access is no longer required.
- AWS CLI identity output showed root credentials (`arn:aws:iam::881027529328:root`). Use a least-privilege IAM identity or role for future routine work.
- Fargate, public IPv4 addresses, and CloudWatch ingestion/storage can incur charges. Clean up resources when finished.
- The log group exists, but actual log events have not yet been confirmed.
- Task health was reported as `UNKNOWN`; ECS still reported steady state and the user confirmed browser reachability. No explicit container health check was configured in the task definition.

## Troubleshooting
- If the app becomes unreachable, confirm Flask binds to `0.0.0.0:8000`, not only `127.0.0.1`.
- Check the security group's TCP 8000 ingress, subnet route to the internet gateway, and task public IP.
- Inspect ECS service events, stopped-task reasons, and CloudWatch log streams before changing settings.
- If the app listens on a different port, update the task definition, register a new revision, and update the service.

## Status
**Fargate deployment and public browser reachability are confirmed.** Screenshot collection, confirmation of actual log events, and security cleanup remain.
