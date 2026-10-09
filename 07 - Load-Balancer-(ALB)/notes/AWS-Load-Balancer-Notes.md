# Project 07 — Notes

## Core Concept

An Application Load Balancer sits between clients and backend servers.

Client
→ ALB
→ Listener
→ Target Group
→ Healthy EC2 Target

## ALB

Application Load Balancer:

- Layer 7
- Handles HTTP/HTTPS
- Uses listeners
- Routes requests to target groups
- Supports multiple Availability Zones
- Performs health checks through target groups

## Listener

A listener waits for connections on a specific port.

Project:

HTTP :80
→ Forward
→ 07-alb-target-group

## Target Group

The target group contains the backend EC2 instances.

Project:

07-alb-target-group
├── Web Server 1
└── Web Server 2

Both targets must be healthy before normal traffic can be distributed to them.

## Health Checks

The ALB checks:

Protocol: HTTP
Port: 80
Path: /

Healthy target
→ eligible for traffic

Unhealthy target
→ removed from normal traffic distribution

## Availability Zones

The ALB uses:

us-east-1a
→ 10.7.1.0/24

us-east-1b
→ 10.7.2.0/24

Using multiple AZs improves fault tolerance.

## Networking

VPC:

10.7.0.0/16

Internet:

Internet
→ Internet Gateway
→ Public Subnets
→ ALB

The public route table contains:

10.7.0.0/16 → local
0.0.0.0/0 → Internet Gateway

## Security Groups

ALB:

HTTP :80
Source: 0.0.0.0/0

Backend:

HTTP :80
Initially open for testing.

Production improvement:

HTTP :80
Source: ALB Security Group

This prevents arbitrary internet clients from directly reaching the EC2 servers.

## DNS

Users access:

ALB DNS name

They should NOT depend on the individual EC2 public IP addresses.

The ALB DNS name can resolve to multiple ALB node IP addresses.

## Troubleshooting Logic

When an ALB cannot be reached, don't randomly change settings.

Check the path:

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

## Important Diagnostic Lesson

`nslookup` proves DNS resolution.

`curl` proves actual network/application connectivity.

HTTP `200 OK` proves the request successfully reached the web server and received a valid response.

## Commands

DNS test:

```cmd
nslookup <ALB-DNS-name>