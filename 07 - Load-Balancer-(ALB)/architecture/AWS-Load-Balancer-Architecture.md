# Project 07 — Architecture

```
                      Internet
                         |
                         v
              Internet Gateway (07-internet-gateway)
                         |
+----------------------------------------------------------+
| VPC: 07-alb-vpc   10.7.0.0/16                            |
|                                                          |
|        Application Load Balancer                         |
|        07-application-load-balancer                      |
|        (internet-facing, IPv4, 2 Availability Zones)     |
|        Security group: 07-alb-security-group (HTTP 80)   |
|                         |                                |
|                  HTTP : Port 80 listener                 |
|                         |                                |
|                  Target group                            |
|                  07-alb-target-group                     |
|                  (health check: HTTP 80, path /)         |
|                    /             \\                       |
|                   v               v                      |
|  +--------------------+   +--------------------+         |
|  | Public subnet      |   | Public subnet      |         |
|  | 10.7.1.0/24        |   | 10.7.2.0/24        |         |
|  | us-east-1a         |   | us-east-1b         |         |
|  |                    |   |                    |         |
|  | EC2 Web Server 1   |   | EC2 Web Server 2   |         |
|  | Apache             |   | Apache             |         |
|  +--------------------+   +--------------------+         |
|     Security group: 07-web-server-security-group         |
+----------------------------------------------------------+
```

