# Project 15 — Flask on Amazon ECS Fargate

## Overview
In Project 14 I put a Flask app in a Docker image and pushed it to Amazon ECR. In this project I ran that same image on Amazon ECS with AWS Fargate, so I didn't have to manage any servers. I wrote a task definition, created a cluster and a service, and opened the app in my browser through the task's public IP on port 8000. I'm still learning ECS, so this README records what I did and what I haven't confirmed yet.

## Stack
Amazon ECS · AWS Fargate · Amazon ECR · Amazon VPC · Amazon CloudWatch Logs · AWS IAM · AWS CLI · Docker image from Project 14

## What I practiced
- Writing and registering an ECS task definition (JSON)
- Creating an ECS cluster and a service
- Running a container on Fargate in my own VPC subnet
- Using the ECR image from Project 14
- Giving the task an execution role and sending logs to CloudWatch
- Opening a security group port for a demo and noting the risk

## Configuration
| Item | Value |
|---|---|
| Region | us-east-1 |
| ECR image | `<ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/project14-webapp:1.0` |
| ECS cluster | `project15-flask-cluster` |
| ECS service | `project15-flask-service`, Fargate, desired count 1 |
| Task definition | `project15-flask`, revision 1 |
| CPU / memory | 256 (0.25 vCPU) / 512 MiB |
| Network mode | `awsvpc`, public IP enabled |
| Container port | 8000 |
| Execution role | `ecsTaskExecutionRole` (`AmazonECSTaskExecutionRolePolicy`) |
| Log group | `/ecs/project15-flask` (`awslogs`, stream prefix `ecs`) |
| Network | my VPC, public subnet `10.0.1.0/24` with an internet gateway route |
| Security group | TCP 8000 open to `0.0.0.0/0` for the demo |

## Project structure
```text
15-ecs-fargate/
├── project/
│   └── task-definition.json    # account ID replaced with <ACCOUNT_ID>
├── documentation/
│   ├── ECS-Fargate-Journal.md
│   └── ECS-Fargate-Notes.md
├── architecture/
│   └── ECS-Fargate-Architecture-Diagram.md
├── screenshots/
│   ├── 01-live-flask-application.png
│   ├── 02-ecs-service-running.png
│   ├── 03-ecs-task-definition.png
│   ├── 04-fargate-task-networking.png
│   ├── 05-cloudwatch-container-logs.png
│   └── 06-ecr-container-image.png
└── README.md
```

## Architecture
```text
Browser --HTTP :8000--> Security group --> Task network interface (awsvpc)
                                                    |
ECR (project14-webapp:1.0) --image pull--> Fargate task (Flask, port 8000)
                                                    |
ECS service (desired 1) in ECS cluster ------------>+--> CloudWatch Logs (/ecs/project15-flask)
Task definition (project15-flask:1)
```

## Screenshots
Add these after hiding the account ID, public IP and any resource IDs I don't want public:

1. `01-live-flask-application.png` — the app in the browser
2. `02-ecs-service-running.png` — service with desired 1, running 1
3. `03-ecs-task-definition.png` — task definition details
4. `04-fargate-task-networking.png` — subnet, security group, network interface
5. `05-cloudwatch-container-logs.png` — real log events (only once I can see them)
6. `06-ecr-container-image.png` — image tag 1.0 in ECR

## What I did
1. Prepared the VPC, public subnet, internet gateway route and security group (TCP 8000).
2. Used the image from Project 14 in ECR (`project14-webapp:1.0`).
3. Made sure `ecsTaskExecutionRole` had `AmazonECSTaskExecutionRolePolicy`.
4. Created the log group `/ecs/project15-flask`.
5. Wrote `task-definition.json` and registered revision 1.
6. Created the cluster `project15-flask-cluster`.
7. Created the service `project15-flask-service` (Fargate, desired count 1, public IP on).
8. The service reached steady state with 1 running task. The task status was RUNNING.
9. Opened `http://<task public IP>:8000` in my browser and the app loaded.

## What the task definition says
- `family`: groups the revisions of this task definition.
- `networkMode: awsvpc`: each task gets its own network interface.
- `requiresCompatibilities: FARGATE`: runs on Fargate.
- `cpu` and `memory`: the task size.
- `executionRoleArn`: lets ECS pull the image and set up logging. This is different from a task role, which is for the app's own AWS calls.
- `portMappings`: container port 8000, which must match the port Flask listens on.
- `logConfiguration`: sends output to CloudWatch Logs.

## Key ideas (in my own words)
- **ECR** stores the image. **ECS** decides what to run. **Fargate** provides the compute without servers for me to manage.
- **Task definition:** the blueprint for the container.
- **Service:** keeps the number of running tasks at the number I asked for.
- **Cluster:** the group that holds services and tasks.
- **Security group and public IP:** decide whether I can reach the task from the internet.
- **Public IP changes:** if ECS replaces the task, the address changes, so it isn't a permanent endpoint.

My one-sentence rule: **ECR stores the image, the task definition describes it, the service keeps it running, and Fargate supplies the compute.**

## Challenge
Not recorded yet. I'll add any problems I hit and how I fixed them.

## Validation checklist
- [x] Task definition registered (revision 1)
- [x] Cluster and service created
- [x] Service at steady state, 1 task running
- [x] App reachable in the browser on port 8000
- [ ] Real log events seen in CloudWatch (log group exists, events not confirmed)
- [ ] Screenshots saved
- [ ] Port 8000 rule restricted after the demo
- [ ] Resources cleaned up

## Notes
- **Task health showed UNKNOWN.** I didn't add a health check to the task definition. ECS still reported steady state and the app loaded.
- **Not done:** load balancer, HTTPS, autoscaling, CI/CD. This project is one task with a public IP, so I won't claim any of those.
- **Security:** port 8000 is open to the whole internet for the demo. I restrict or remove the rule afterwards.
- **Root credentials:** my AWS CLI was using the root account. Lesson learned: I will create an IAM user with only the permissions I need and use that.
- **Cost:** a running Fargate task, a public IPv4 address and log storage can all charge. When I'm finished I set the service's desired count to 0, then delete the service and cluster, and check Billing.

Documentation was written with AI assistance (Claude) for structure and clarity. I did the lab myself and checked what is written here against what I did.
