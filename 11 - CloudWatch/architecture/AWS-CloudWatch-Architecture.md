# Project 11 — Architecture

```
        +----------------------------------+
        | EC2: Monitored-App-Server        |
        | Amazon Linux 2023                |
        | IAM role: EC2-CloudWatch-        |
        |           Monitoring-Role        |
        +----------------+-----------------+
                         |
                         v
        +----------------------------------+
        | Unified CloudWatch Agent         |
        | memory, disk, /var/log/messages  |
        +----------------+-----------------+
                         |  (also: EC2 sends CPU by itself)
                         v
        +----------------------------------+
        |        Amazon CloudWatch         |
        +------+-------------+-------------+
               |             |             |
               v             v             v
        +-----------+  +-----------+  +----------------------+
        | Metrics   |  | Logs      |  | Alarm                |
        | CWAgent   |  | /aws/ec2/ |  | CPU > 70%, 1 minute  |
        | mem, disk |  | system-   |  | (no SNS connected)   |
        |           |  | messages  |  |                      |
        +-----+-----+  +-----+-----+  +----------+-----------+
              |              |                   |
              +--------------+-------------------+
                             |
                             v
              +--------------------------------+
              | Dashboard                      |
              | EC2-System-Observability-      |
              | Dashboard                      |
              +--------------------------------+
```

