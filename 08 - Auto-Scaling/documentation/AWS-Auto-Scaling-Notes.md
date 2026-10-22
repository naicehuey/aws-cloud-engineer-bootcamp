# Project 08 — Learning Notes

## Core architecture
```text
                 Users
                   │
                   ▼
        Application Load Balancer
                   │
                   ▼
             Target Group
             ┌─────┴─────┐
             ▼           ▼
          EC2 #1       EC2 #2
             ▲           ▲
             └─────┬─────┘
                   │
          Auto Scaling Group
                   ▲
                   │
            Launch Template
```

The setup spans two Availability Zones (`us-east-1a` and `us-east-1b`) for availability and fault tolerance.

## Core components

### Application Load Balancer (ALB)
Shares incoming web traffic across EC2 instances. Mine: `web-app-alb`.
```text
User traffic -> ALB -> healthy instances
```

### Target group
Holds the instances the ALB sends traffic to and reports their health. Mine: `web-app-tg`.
```text
ALB -> Target Group -> healthy EC2 instances
```

### Auto Scaling Group (ASG)
Keeps the right number of EC2 instances and adjusts it using the scaling policy. Mine: `web-app-asg`.
```text
Scale out -> add capacity
Scale in  -> remove capacity
```

### Launch Template
Defines how new instances are built. The ASG uses it every time it launches an instance. Mine: `web-server-template`.

### User Data
A script that runs when a new instance first starts. It sets up the instance automatically, so I don't configure every server by hand.

### Availability Zones
Using more than one improves availability and reduces dependence on a single zone.

## Scaling policy and CloudWatch alarms
I used a target tracking policy based on CPU. It created two CloudWatch alarms:

| Alarm | Meaning |
|---|---|
| `AlarmHigh` | CPU is high, so the ASG scales out |
| `AlarmLow` | CPU is low, so the ASG scales in |

When `AlarmLow` showed "In alarm", it was the signal that the group could scale in.

## How the services relate
```text
Launch Template (what an instance looks like)
      ↓
Auto Scaling Group (how many instances)
      ↓
EC2 instances
      ↓
Target Group (which ones get traffic)
      ↓
Application Load Balancer (shares the traffic)
```

When demand changes:
```text
High CPU  -> Scale out -> more EC2 capacity
Low CPU   -> Scale in  -> less EC2 capacity
```

## Remember when something fails
I saw an HTTP 202 turn into a 403 and I didn't write down the cause. Next time I'll record:
1. The exact HTTP status
2. The ALB listener configuration
3. The target group health
4. What the EC2 instance or application returned
5. Relevant logs
6. Whether the answer comes from the ALB or from the application

Then I'll find the layer that's failing.

## Cost awareness
An ALB charges by the hour, and the ASG keeps instances running. Delete the ASG first (terminating an instance by hand just makes the ASG launch a new one), then the ALB and the target group. Check Billing.

## Self-test
1. What does an ALB do?
2. What is a target group?
3. What does an Auto Scaling Group do?
4. Why use a Launch Template?
5. Why use more than one Availability Zone?
6. What happens during scale-out and scale-in?
7. How does the ALB know which instances can get traffic?
8. What are `AlarmHigh` and `AlarmLow`?

### Answers
1. It shares incoming web traffic across registered targets.
2. A group of targets the load balancer sends traffic to, with their health status.
3. It manages EC2 capacity and adds or removes instances based on the scaling policy.
4. It gives a repeatable recipe for the instances the ASG launches.
5. To improve availability and avoid depending on one zone.
6. Scale-out launches more instances. Scale-in removes instances when demand is lower.
7. It uses the target group and its health checks.
8. The two CloudWatch alarms created by the target tracking policy: one triggers scale-out and the other scale-in.

## One-sentence memory rule
> **The Launch Template defines the server, the ASG controls the fleet, the target group tracks the targets, and the ALB distributes the traffic.**
