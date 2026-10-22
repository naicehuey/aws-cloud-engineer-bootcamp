# Project 15 — Project Journal

**Date:** Not recorded

## Goal
Run the Flask container from Project 14 on ECS Fargate and reach it from my browser.

## Work completed
1. Prepared the VPC, public subnet, internet gateway route and security group (TCP 8000).
2. Reused the ECR image `project14-webapp:1.0`.
3. Checked `ecsTaskExecutionRole` had `AmazonECSTaskExecutionRolePolicy`.
4. Created the log group `/ecs/project15-flask`.
5. Registered the task definition `project15-flask` revision 1.
6. Created the cluster and the service (desired count 1).
7. ECS reached steady state with 1 running task, and the app loaded in my browser.

## What I learned
- A task definition describes the container, and a service keeps it running.
- Fargate means I don't manage servers, but I still manage networking and permissions.
- The execution role is for ECS to pull the image and set up logs, and a task role is for the app's own AWS calls.
- The container port in the task definition must match the port Flask listens on.
- A public IP on a task isn't permanent. It can change when ECS replaces the task.
- Steady state and a loading page are good signs, but they don't prove logging works.

## Issue and lesson
Task health showed UNKNOWN because I hadn't configured a health check. I also never confirmed log events in CloudWatch. Lesson: a log group existing doesn't mean logs are arriving, so I check the log stream for real events before I claim it.

## Mistakes to avoid (for my future projects)
- Using root credentials for the AWS CLI.
- Leaving a port open to `0.0.0.0/0` after the demo.
- Saying logging works when I only created the log group.
- Leaving a Fargate service running with desired count 1.

## Evidence
Screenshots 01 to 06: live app, service running, task definition, networking, logs, ECR image.

## Outcome
The Flask app ran on Fargate and loaded in the browser. Still to do: confirm the logs, save the screenshots, close the port and clean up.

## Cost reminder
Fargate, a public IPv4 address and log storage can charge. Set the service to 0 tasks, delete the service and cluster, and check Billing.
