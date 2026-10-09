# AWS Auto Scaling & Elastic Load Balancing — Notes

## Core Architecture

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

The architecture is deployed across multiple Availability Zones for high availability and fault tolerance.

## Core Components

### Application Load Balancer (ALB)

**Purpose:** Distributes incoming web traffic across EC2 instances.

Key idea:

```text
User traffic → ALB → healthy instances
```

The project verified traffic distribution through the ALB.

---

### Target Group

**Purpose:** Holds the instances that the ALB sends traffic to and provides health-check status.

Key idea:

```text
ALB → Target Group → Healthy EC2 instances
```

The project verified healthy target registration.

---

### Auto Scaling Group (ASG)

**Purpose:** Maintains the required number of EC2 instances and adjusts capacity according to the configured scaling policy.

This project demonstrated both:

```text
Scale Out → increase capacity
Scale In  → decrease capacity
```

The scaling behavior was demonstrated using CPU metrics.

---

### Launch Template

**Purpose:** Defines how new EC2 instances are provisioned.

It provides the configuration used when the ASG launches instances.

The project used Launch Template based automated provisioning with User Data.

---

### User Data

**Purpose:** Bootstraps newly launched EC2 instances automatically.

This allows instances launched by the ASG to receive their required initial configuration without manually configuring every server.

---

### Availability Zones

The architecture spans multiple Availability Zones.

Purpose:

- Improve availability.
- Reduce dependence on a single Availability Zone.
- Support fault tolerance.

---

# Service Relationships

## Launch Template → ASG

The Launch Template defines **what an instance should look like**.

The ASG manages **how many instances should exist**.

```text
Launch Template
      ↓
   ASG
      ↓
EC2 instances
```

## ASG → Target Group

Instances launched and managed by the ASG can be registered with the target group so that they can receive load-balanced traffic.

```text
ASG
 ↓
EC2
 ↓
Target Group
```

## ALB → Target Group

The ALB sends requests to the targets registered in the target group.

```text
Internet
   ↓
  ALB
   ↓
Target Group
   ↓
 EC2
```

## ASG → Scaling

When the configured scaling condition is met:

```text
High demand / CPU
        ↓
    Scale Out
        ↓
More EC2 capacity
```

When demand falls:

```text
Lower demand / CPU
        ↓
     Scale In
        ↓
Less EC2 capacity
```

# Verification Checklist

Use this checklist when rebuilding the project:

- [ ] Launch Template created
- [ ] ALB provisioned
- [ ] ALB active
- [ ] Target Group created
- [ ] EC2 instances registered
- [ ] Target health checks passing
- [ ] Traffic successfully distributed
- [ ] Scale-out demonstrated
- [ ] Scale-in demonstrated
- [ ] Screenshots captured

# Screenshot Evidence

| Evidence | File |
|---|---|
| Launch Template | `screenshots/01-launch-template-configuration.png` |
| ALB active | `screenshots/02-alb-active-state.png` |
| Healthy targets | `screenshots/03-target-group-healthy-instances.png` |
| Traffic distribution | `screenshots/04-load-balancer-traffic-distribution.png` |
| Scale-out | `screenshots/05-auto-scaling-scale-out.png` |
| Scale-in | `screenshots/06-auto-scaling-scale-in.png` |

# Important Troubleshooting Note

An error involving **HTTP 202 falling back to 403** was reported during the project, but the supplied README does not document its exact cause or resolution.

Do not memorize a guessed explanation. When encountering the error again, capture:

1. Exact HTTP status.
2. ALB listener configuration.
3. Target group health.
4. EC2/application response.
5. Relevant logs.
6. Whether the response comes from the ALB or the application.

Then isolate the failing layer.

# Interview Questions

### 1. What does an ALB do?

It distributes incoming application/web traffic across registered targets.

### 2. What is a Target Group?

It defines the targets that the load balancer sends traffic to and provides health-check information.

### 3. What does an Auto Scaling Group do?

It manages EC2 capacity and can automatically add or remove instances according to scaling conditions.

### 4. Why use a Launch Template?

It provides a repeatable configuration for instances launched by services such as an Auto Scaling Group.

### 5. Why deploy across multiple Availability Zones?

To improve availability and reduce dependence on a single Availability Zone.

### 6. What happens during scale-out?

The ASG launches additional EC2 capacity according to its scaling configuration.

### 7. What happens during scale-in?

The ASG reduces EC2 capacity when the scaling condition calls for fewer instances.

### 8. How does the ALB know which instances can receive traffic?

It uses the Target Group and its health checks.

# One-Sentence Memory Rule

> **Launch Template defines the server, ASG controls the fleet, Target Group tracks the targets, and ALB distributes the traffic.**
