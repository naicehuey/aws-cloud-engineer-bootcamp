# AWS Auto Scaling & Elastic Load Balancing — Project Journal

## Project

**AWS Auto Scaling & Elastic Load Balancing Architecture**

## Objective

Build a high-availability, fault-tolerant web architecture on AWS using an Application Load Balancer (ALB) and an Auto Scaling Group (ASG) across multiple Availability Zones.

## What I Built

The project combined three major capabilities:

1. **Load balancing** — the Application Load Balancer distributes incoming traffic across EC2 instances.
2. **Dynamic scaling** — the Auto Scaling Group performs automatic scale-out and scale-in based on CPU metrics.
3. **Automated provisioning** — EC2 instances are bootstrapped using a Launch Template and User Data.

The README describes the completed architecture as a multi-AZ AWS web architecture designed for high availability and fault tolerance.

## Build Evidence

### 1. Launch Template

The Launch Template configuration was completed and documented with:

`screenshots/01-launch-template-configuration.png`

The Launch Template is the provisioning foundation for instances created by the Auto Scaling Group.

### 2. Application Load Balancer

The Application Load Balancer was provisioned and reached an active state.

Evidence:

`screenshots/02-alb-active-state.png`

### 3. Target Group and Health Checks

The target group successfully registered healthy instances and health checks were verified.

Evidence:

`screenshots/03-target-group-healthy-instances.png`

### 4. Traffic Distribution

Traffic distribution through the load balancer was successfully verified.

Evidence:

`screenshots/04-load-balancer-traffic-distribution.png`

This demonstrates that the ALB was able to distribute requests across the instances behind it.

### 5. Automated Scale-Out

The Auto Scaling Group successfully demonstrated automated scale-out under load.

Evidence:

`screenshots/05-auto-scaling-scale-out.png`

This is important because it demonstrates that the architecture can increase capacity when demand increases.

### 6. Automated Scale-In

The Auto Scaling Group also successfully demonstrated automated scale-in.

Evidence:

`screenshots/06-auto-scaling-scale-in.png`

This demonstrates that capacity can be reduced after the additional demand is no longer present.

## What I Learned

The project connected several AWS concepts into one working architecture:

```text
Launch Template
       ↓
Auto Scaling Group
       ↓
EC2 Instances
       ↓
Target Group
       ↓
Application Load Balancer
       ↓
Users
```

The architecture also uses multiple Availability Zones so that the web workload is not dependent on a single Availability Zone.

The most important practical lesson is that these services are not isolated. The Launch Template provides the instance configuration, the ASG manages instance capacity, the Target Group tracks the instances that receive traffic, and the ALB distributes user requests.

## Troubleshooting / Unresolved Issue

During the work, an error involving **HTTP 202 falling back to 403** was encountered. The exact cause and final resolution are not documented in the supplied README, so this journal does not claim a definitive root cause.

For future troubleshooting, record the exact response, ALB/target-group status, application response, and relevant logs before changing multiple components.

## Project Result

The supplied README documents successful completion of:

- ALB provisioning
- Target group health checks
- Traffic distribution
- Automated scale-out
- Automated scale-in
- Launch Template based provisioning

Overall, this project demonstrates a working AWS Auto Scaling and Elastic Load Balancing architecture across multiple Availability Zones.
