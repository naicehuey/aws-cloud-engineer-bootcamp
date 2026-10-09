                         INTERNET
                            │
                            ▼
                ┌─────────────────────┐
                │ Application Load    │
                │ Balancer            │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Target Group        │
                │                     │
                │ Healthy targets     │
                └───────┬───────┬─────┘
                        │       │
                        ▼       ▼
                   EC2 #1     EC2 #2
                        ▲       ▲
                        │       │
                ┌───────┴───────┴─────┐
                │ Auto Scaling Group   │
                └──────────┬──────────┘
                           ▲
                           │
                ┌──────────┴──────────┐
                │ Launch Template     │
                │ "How to build an    │
                │ EC2 instance"       │
                └─────────────────────┘