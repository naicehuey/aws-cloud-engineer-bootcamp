# Project 15 — Architecture

```text
                     User browser
                          |
                          |  HTTP :8000
                          v
              +-------------------------+
              | Security group          |
              | TCP 8000 (demo only)    |
              +------------+------------+
                           |
        VPC / public subnet (10.0.1.0/24, internet gateway route)
                           |
                           v
              +-------------------------+
              | Task network interface  |
              | (awsvpc, public IP)     |
              +------------+------------+
                           |
                           v
 +-------------+   +-------------------------+   +--------------------+
 | ECR         |-->| Fargate task            |-->| CloudWatch Logs    |
 | project14-  |   | container: Flask :8000  |   | /ecs/project15-    |
 | webapp:1.0  |   | CPU 256, memory 512     |   | flask              |
 +-------------+   +------------+------------+   +--------------------+
   image pull                   ^
                                |
              +-----------------+------------------+
              | ECS service (desired count 1)      |
              | project15-flask-service            |
              | in cluster project15-flask-cluster |
              | task definition project15-flask:1  |
              +------------------------------------+

 IAM execution role (ecsTaskExecutionRole): lets ECS pull the image
 and set up logging.
```
