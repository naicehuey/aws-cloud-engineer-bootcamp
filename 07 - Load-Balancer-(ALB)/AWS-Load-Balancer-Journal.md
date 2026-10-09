# Project 07 — Journal

## Project

Application Load Balancer

## Objective

Build an internet-facing Application Load Balancer that distributes HTTP traffic between two EC2 web servers located in different Availability Zones.

## What I Built

I created:

- A dedicated VPC
- Two public subnets
- An Internet Gateway
- A public route table
- Two EC2 web servers
- An ALB security group
- A web server security group
- A target group
- An Application Load Balancer
- An HTTP listener

The two EC2 servers were placed in different Availability Zones.

## Initial Experience

The architecture looked simple:

Internet
→ ALB
→ Target Group
→ EC2 Servers

However, when I first opened the ALB DNS name in Microsoft Edge, the browser timed out.

This created uncertainty because the AWS console configuration appeared correct.

## Troubleshooting

Instead of rebuilding the project, I checked the architecture one component at a time.

### 1. ALB Security Group

Confirmed HTTP TCP port 80 was allowed.

Result: PASS.

### 2. ALB Attachment

Confirmed the correct security group was attached to the ALB.

Result: PASS.

### 3. Public Routes

Confirmed both ALB subnets had a default route:

`0.0.0.0/0 → Internet Gateway`

Result: PASS.

### 4. Network ACL

Confirmed the network ACL was not blocking the traffic.

Result: PASS.

### 5. ALB Status

Confirmed the ALB was:

- Active
- Internet-facing
- IPv4

Result: PASS.

### 6. Listener

Confirmed:

HTTP :80
→ 07-alb-target-group

Result: PASS.

### 7. Network Mapping

Confirmed the ALB was deployed across:

- us-east-1a
- us-east-1b

With:

- 10.7.1.0/24
- 10.7.2.0/24

Result: PASS.

### 8. Internet Gateway

Confirmed:

`07-internet-gateway`

was attached to:

`07-alb-vpc`

Result: PASS.

### 9. EC2 Security Groups

Both web servers had HTTP port 80 allowed and both instances passed their EC2 status checks.

Result: PASS.

### 10. DNS and Connectivity Test

I used:

```cmd
nslookup <ALB-DNS-name>