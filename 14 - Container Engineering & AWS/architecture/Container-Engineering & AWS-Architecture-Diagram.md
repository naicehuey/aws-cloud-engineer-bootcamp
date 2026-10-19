                              Developer / PowerShell[cite: 1]
                                         │
                                         ▼
                         Flask Source Code & Dockerfile[cite: 1]
                                         │
                                         ▼
                              Local Docker Image[cite: 1]
                            (project14-webapp:1.0)[cite: 1]
                                         │
         ┌──────────────────────┴──────────────────────┐
         ▼                                                              ▼
  Docker Compose[cite: 1]                                  Amazon ECR Registry[cite: 1]
(Local Container)[cite: 1]                               (Cloud-Hosted Image)[cite: 1]
 HTTP : Port 8000[cite: 1]                                               │
         │                                                               ▼
         ▼                                                 Project 15: ECS & Fargate[cite: 1]
Browser / REST Client[cite: 1]