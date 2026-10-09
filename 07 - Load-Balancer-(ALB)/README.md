# Project 07 — Application Load Balancer

## Overview

This project demonstrates how to distribute HTTP traffic across multiple EC2 web servers using an AWS Application Load Balancer (ALB).

The application is deployed across two Availability Zones for improved availability.

## Architecture

Internet
   |
Internet Gateway
   |
Application Load Balancer
   |
HTTP :80 Listener
   |
07-alb-target-group
   |-------------------|
   |                   |
EC2 Web Server 1   EC2 Web Server 2
us-east-1a          us-east-1b
   |                   |
Apache              Apache

## AWS Resources

- VPC: `07-alb-vpc`
- VPC CIDR: `10.7.0.0/16`
- Internet Gateway: `07-internet-gateway`
- Public Subnet 1: `10.7.1.0/24`
- Public Subnet 2: `10.7.2.0/24`
- Application Load Balancer: `07-application-load-balancer`
- ALB Security Group: `07-alb-security-group`
- Target Group: `07-alb-target-group`
- Web Server Security Group: `07-web-server-security-group`
- EC2 Web Server 1: `07-alb-web-server-1`
- EC2 Web Server 2: `07-alb-web-server-2`

## Configuration

### Load Balancer

- Type: Application Load Balancer
- Scheme: Internet-facing
- IP address type: IPv4
- Availability Zones: 2
- Listener: HTTP :80

### Listener

The HTTP listener forwards incoming requests to:

`07-alb-target-group`

### Target Group

- Target type: Instances
- Protocol: HTTP
- Port: 80
- Health check path: `/`
- Registered targets: 2
- Target health: Healthy

### Web Servers

Both EC2 instances run Apache HTTP Server.

Each server returns a different response so that load balancing can be observed.

Server 1:

`Server 1 - Application Load Balancer Project`

Server 2:

`Server 2 - Application Load Balancer Project`

## Security

The ALB security group allows HTTP traffic on port 80 from the internet.

The web server security group initially allows HTTP traffic on port 80 so the application can be tested.

A production implementation should restrict the web server HTTP rule to traffic originating from the ALB security group rather than allowing `0.0.0.0/0`.

## Verification

DNS resolution was verified using:

```text
nslookup <ALB-DNS-name>