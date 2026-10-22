# Project 14 — Architecture

```

           Developer / PowerShell
                     |
                     v
        Flask Source Code \\\\\\\\\\\\\\\& Dockerfile
                     |
                     v
              Local Docker Image
            (project14-webapp:1.0)
                     |
        +------------+-------------+
        |                          |
        v                          v

Docker Compose            Amazon ECR Registry
(Local Container)         (Cloud-Hosted Image)
HTTP : Port 8000                 |
|                          v
v                 Project 15: ECS \\\\\\\& Fargate

Browser / REST Client

```

