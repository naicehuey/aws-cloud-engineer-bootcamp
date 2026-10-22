# Project 07 — Learning Notes

## Core concept
An Application Load Balancer sits between clients and backend servers.

```text
Client -> ALB -> Listener -> Target Group -> Healthy EC2 target
```

## ALB
- Works at layer 7 and handles HTTP/HTTPS
- Uses listeners
- Routes requests to target groups
- Supports multiple Availability Zones
- Checks health through the target group

## Listener
A listener waits for connections on a specific port.

```text
HTTP :80 -> Forward -> 07-alb-target-group
```

## Target group
The target group holds the backend EC2 instances.

```text
07-alb-target-group
├── Web Server 1  (us-east-1a)
└── Web Server 2  (us-east-1b)
```

Both targets must be healthy before normal traffic is shared between them.

## Health checks
```text
Protocol: HTTP
Port: 80
Path: /
```

- Healthy target: eligible for traffic
- Unhealthy target: left out of normal traffic

## Availability Zones
```text
us-east-1a -> 10.7.1.0/24
us-east-1b -> 10.7.2.0/24
```

Using more than one Availability Zone improves fault tolerance.

## Networking
```text
VPC: 10.7.0.0/16

Internet -> Internet Gateway -> Public subnets -> ALB
```

The public route table:
```text
10.7.0.0/16 -> local
0.0.0.0/0   -> Internet Gateway
```

## Security groups
ALB:
```text
HTTP :80   Source: 0.0.0.0/0
```

Backend servers:
```text
HTTP :80   (open for testing in this project)
```

Better for a real setup:
```text
HTTP :80   Source: the ALB security group
```
This stops arbitrary internet clients from reaching the servers directly.

## DNS
Users reach the ALB DNS name. They shouldn't depend on the individual EC2 public IP addresses. The ALB DNS name can resolve to several ALB node IP addresses.

## Troubleshooting logic
When an ALB can't be reached, don't change settings at random. Check the path in order:

```text
Client
  ↓
DNS
  ↓
Internet
  ↓
Internet Gateway
  ↓
ALB subnet
  ↓
ALB security group
  ↓
Listener
  ↓
Target group
  ↓
Target health
  ↓
EC2 security group
  ↓
Web server
```

## Diagnostic lesson
- `nslookup` shows that DNS resolves.
- `curl` shows that a real network and application connection works.
- HTTP `200 OK` shows that the request reached the web server and got a valid answer.

## Commands
DNS test:
```cmd
nslookup <ALB-DNS-name>
```

Apache on Amazon Linux (on each web server):
```bash
sudo systemctl start httpd
sudo systemctl enable httpd
sudo systemctl status httpd
echo "<h1>Server 1 - Application Load Balancer Project</h1>" | sudo tee /var/www/html/index.html
```
Server 2 uses the same commands with "Server 2" in the message. I need to check the message before I run the command on the second server.

## Cost awareness
An ALB charges by the hour while it exists, and the instances cost money while they run. Delete the ALB, the target group and the instances when I'm finished, and check Billing.

## Self-test
1. What does an ALB do?
2. What is the difference between a listener and a target group?
3. What does a health check do?
4. Why use two Availability Zones?
5. Why should visitors use the ALB DNS name and not the servers' IPs?
6. What is the difference between `nslookup` and `curl` when I troubleshoot?
7. How should the web server security group be set in a real setup?

### Answers
1. It shares incoming HTTP/HTTPS requests between healthy servers.
2. A listener waits for connections on a port and decides where to forward them. A target group holds the servers that receive them.
3. It checks whether a server is working, so only healthy servers get traffic.
4. If one zone has a problem, the other can keep serving.
5. The ALB address stays the same and the ALB knows which servers are healthy. Server IPs can change or fail.
6. `nslookup` checks DNS. `curl` checks a real connection to the application.
7. Allow HTTP only from the ALB security group, not from `0.0.0.0/0`.
