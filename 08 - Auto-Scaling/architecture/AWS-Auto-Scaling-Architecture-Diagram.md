# Project 08 — Architecture

```
                         INTERNET
                            |
                            v
              +-------------------------------+
              | Application Load Balancer     |
              | web-app-alb (internet-facing) |
              +---------------+---------------+
                              |
                              v
              +-------------------------------+
              | Target Group: web-app-tg      |
              | (HTTP 80, health checks)      |
              +-------+---------------+-------+
                      |               |
                      v               v
              +-------------+   +-------------+
              | EC2 #1      |   | EC2 #2      |
              | us-east-1a  |   | us-east-1b  |
              +------+------+   +------+------+
                     ^                 ^
                     |                 |
              +------+-----------------+------+
              | Auto Scaling Group            |
              | web-app-asg                   |
              | Scales out / in on CPU        |
              | (CloudWatch AlarmHigh/Low)    |
              +---------------+---------------+
                              ^
                              |
              +---------------+---------------+
              | Launch Template               |
              | web-server-template           |
              | "How to build an EC2 instance"|
              +-------------------------------+
```

