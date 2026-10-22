# Project 15 Architecture Diagram

```mermaid
flowchart TD
    User[User browser]
    IP[Public IP observed<br/>18.206.87.153:8000]
    SG[Security group<br/>TCP 8000 ingress]
    ENI[Task network interface<br/>awsvpc]
    Task[Fargate task<br/>project15-flask]
    Flask[Flask container<br/>port 8000]
    Service[ECS service<br/>project15-flask-service<br/>desired count 1]
    Cluster[ECS cluster<br/>project15-flask-cluster]
    TD[Task definition<br/>project15-flask:1]
    ECR[Amazon ECR<br/>project14-webapp:1.0]
    Role[IAM execution role<br/>ecsTaskExecutionRole]
    Logs[CloudWatch Logs<br/>/ecs/project15-flask]
    VPC[VPC and public subnet<br/>10.0.1.0/24<br/>internet gateway route]

    User -->|HTTP request| IP
    IP --> SG
    SG --> ENI
    ENI --> Task
    Task --> Flask
    Service --> Task
    Cluster --> Service
    TD --> Service
    ECR -->|Image pull| Task
    Role -->|ECR and logging setup permissions| Task
    Flask -->|stdout/stderr via awslogs| Logs
    VPC --- ENI
```

## How to read it
- Browser traffic reaches the task's public IP on TCP 8000.
- The task is managed by an ECS service in an ECS cluster.
- The task definition specifies image, port, CPU/memory, execution role and log configuration.
- ECR stores the image pulled at task startup.
- The task receives an ENI in the VPC subnet.
- Container logging is configured for CloudWatch Logs; actual events still need verification.
- The public IP may change if the task is replaced.
