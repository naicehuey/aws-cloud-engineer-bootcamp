# AWS Auto Scaling & Elastic Load Balancing Architecture

## Overview
A high-availability, fault-tolerant web architecture deployed on AWS using an Application Load Balancer (ALB) and an Auto Scaling Group (ASG) across multiple Availability Zones.

## Key Features
- **Load Balancing:** ALB distributes traffic across instances.
- **Dynamic Scaling:** Automatic Scale-Out/Scale-In based on CPU metrics.
- **Automated Provisioning:** EC2 instances bootstrapped via Launch Templates and User Data scripts.

## Architecture Screenshots

### 1. Launch Template Configuration
![Launch Template](./screenshots/01-launch-template-configuration.png)

### 2. Load Balancer Provisioning
![ALB Overview](./screenshots/02-alb-active-state.png)

### 3. Health Checks & Target Group Registration
![Target Group](./screenshots/03-target-group-healthy-instances.png)

### 4. Traffic Distribution Verification
![Load Balancing Proof](./screenshots/04-load-balancer-traffic-distribution.png)

### 5. Automated Scale-Out Under Load
![Scale Out](./screenshots/05-auto-scaling-scale-out.png)

### 6. Automated Scale-In
![Scale In](./screenshots/06-auto-scaling-scale-in.png)