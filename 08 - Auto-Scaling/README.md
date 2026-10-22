# Project 08 — Auto Scaling & Load Balancing

## Overview
My first lab with Auto Scaling. I combined three things I had been learning separately: a Launch Template (how to build a server), an Auto Scaling Group (how many servers to run) and an Application Load Balancer (how to share traffic between them). The servers sit in two Availability Zones, and the Auto Scaling Group adds or removes servers automatically based on CPU use. I'm a beginner with Auto Scaling, so this README records what I did and what I understood so far.

## Stack
Amazon EC2 Auto Scaling · Launch Templates · Application Load Balancer · Target Groups · Amazon CloudWatch · Amazon EC2 · AWS Management Console

## What I practiced
- Creating a Launch Template with User Data to set up new servers automatically
- Creating an Application Load Balancer and a target group
- Creating an Auto Scaling Group across two Availability Zones
- Using a target tracking scaling policy based on CPU
- Watching scale-out and scale-in happen
- Reading the CloudWatch alarms that drive the scaling

## AWS resources
| Resource | Name | Details |
|---|---|---|
| Launch Template | `web-server-template` | Version 1, `t3.micro`, key pair from Project 03 |
| Load balancer | `web-app-alb` | Application, internet-facing, IPv4, `us-east-1a` and `us-east-1b` |
| Target group | `web-app-tg` | Instances, HTTP 80, 2 registered targets |
| Auto Scaling Group | `web-app-asg` | Target tracking policy based on CPU |
| CloudWatch alarms | `TargetTracking-web-app-asg-AlarmHigh` and `AlarmLow` | Created automatically by the scaling policy |

I used my default VPC for this project.

## Architecture
```text
Users
  |
  v
Application Load Balancer
  |
  v
Target Group
  |
  +-------+-------+
  |               |
  v               v
EC2 #1          EC2 #2
  ^               ^
  +-------+-------+
          |
Auto Scaling Group
          ^
          |
Launch Template
```

## Screenshots

### 1. Launch Template configuration
![Launch Template](./screenshots/01-launch-template-configuration.png)

### 2. Load balancer provisioning
![ALB Overview](./screenshots/02-alb-active-state.png)

### 3. Health checks and target group registration
![Target Group](./screenshots/03-target-group-healthy-instances.png)

### 4. Traffic distribution check
![Load Balancing Proof](./screenshots/04-load-balancer-traffic-distribution.png)

### 5. Scale-out under load
![Scale Out](./screenshots/05-auto-scaling-scale-out.png)

### 6. Scale-in
![Scale In](./screenshots/06-auto-scaling-scale-in.png)

## What I did
1. Created the Launch Template `web-server-template` (`t3.micro`) with User Data so new servers set themselves up.
2. Created the Application Load Balancer `web-app-alb` across `us-east-1a` and `us-east-1b` and waited until it was Active.
3. Created the target group `web-app-tg` (HTTP 80) and checked that its two targets were Healthy.
4. Created the Auto Scaling Group `web-app-asg` from the Launch Template and attached it to the target group.
5. Added a target tracking scaling policy based on CPU.
6. Opened the load balancer's address in a browser. It answered, and I saw two different pages ("Hello from AWS Auto Scaling!" and "It works!"), so requests were reaching both servers.
7. Put load on the servers and watched the Auto Scaling Group scale out.
8. When the load was gone, watched it scale in.
9. Checked the two CloudWatch alarms the policy created (`AlarmHigh` and `AlarmLow`).
10. Organised the screenshots and wrote this documentation.

## Key ideas (in my own words)
- **Launch Template:** defines what a new server looks like (the image, size, key pair and setup). It's the recipe.
- **User Data:** a script that runs when a server first starts, so I don't have to set up each server by hand.
- **Auto Scaling Group (ASG):** keeps the right number of servers running and adds or removes servers when needed.
- **Scale-out and scale-in:** scale-out adds servers when demand is high. Scale-in removes servers when it drops.
- **Target tracking policy:** I choose a target (CPU use) and the ASG adds or removes servers to stay close to it. It creates two CloudWatch alarms for me, one high and one low.
- **Target group and ALB:** the ASG's servers register in the target group, and the ALB sends traffic only to healthy ones.
- **Multiple Availability Zones:** my servers aren't depending on one zone.

My one-sentence rule: **the Launch Template defines the server, the ASG controls the fleet, the target group tracks the targets, and the ALB distributes the traffic.**

## Challenge
At one point I saw an error where an HTTP 202 turned into a 403. I didn't record the exact cause or fix at the time, so I'm not sure what it was. Next time I'll write down the exact response, the target group health and what the application returned before I change anything.

## Validation checklist
- [x] Launch Template created
- [x] Application Load Balancer created and Active
- [x] Target group created with healthy targets
- [x] Auto Scaling Group created across two Availability Zones
- [x] Scaling policy based on CPU created
- [x] Traffic reached the servers through the load balancer
- [x] Scale-out demonstrated
- [x] Scale-in demonstrated
- [x] Screenshots captured
- [ ] HTTPS (not set up in this project)

## Notes
An Application Load Balancer charges by the hour while it exists, and the Auto Scaling Group keeps instances running, so I delete the Auto Scaling Group first, then the load balancer and the target group, when I'm finished. If I only terminate an instance, the group launches a new one. I'm still learning Auto Scaling and want to practice it more.

Documentation was written with AI assistance (Claude) for structure and clarity. I did the lab in the AWS Console myself and checked what is written here against what I did.
