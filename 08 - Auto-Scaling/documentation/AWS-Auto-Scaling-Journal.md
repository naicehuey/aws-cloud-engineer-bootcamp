# Project 08 — Project Journal

**Date:** September 28, 2026

## Goal
Build a web setup that can add and remove servers by itself, with a load balancer sharing the traffic, across two Availability Zones.

## Work completed
1. Created the Launch Template `web-server-template` (version 1, `t3.micro`) with User Data to set up new servers.
2. Created the Application Load Balancer `web-app-alb` (internet-facing, IPv4, `us-east-1a` and `us-east-1b`) and waited for it to be Active.
3. Created the target group `web-app-tg` (HTTP 80) and checked that both targets were Healthy.
4. Created the Auto Scaling Group `web-app-asg` from the Launch Template and attached it to the target group.
5. Added a target tracking scaling policy based on CPU. It created the CloudWatch alarms `AlarmHigh` and `AlarmLow`.
6. Opened the load balancer's address and saw two different pages, so requests reached both servers.
7. Watched the Auto Scaling Group scale out under load, then scale in when the load went away.

## What I learned
- These services work together: the Launch Template defines the server, the ASG controls how many, the target group tracks them and the ALB shares traffic.
- User Data lets new servers set themselves up with no manual work.
- A target tracking policy creates the CloudWatch alarms for me. `AlarmHigh` is for scaling out and `AlarmLow` is for scaling in.
- Scaling out adds capacity when demand goes up, and scaling in removes it when demand goes down.
- Using two Availability Zones means I'm not depending on one zone.

My one-sentence rule: **the Launch Template defines the server, the ASG controls the fleet, the target group tracks the targets, and the ALB distributes the traffic.**

## Issue and lesson
At one point I saw an error where an HTTP 202 turned into a 403. I didn't record the exact cause or fix, so I'm not sure what it was.

Lesson: when something unexpected happens, write down the exact response, the target group health, what the application returned and which layer it came from, before I change several things at once.

## Mistakes to avoid (for my future projects)
- Changing many settings at once when something fails.
- Forgetting to write down errors and fixes while I work.
- Terminating an instance by hand when an Auto Scaling Group manages it. The group just launches another one.
- Leaving the ASG, ALB or instances running when I'm finished.

## Evidence
Screenshots: Launch Template, ALB in the Active state, target group with healthy instances, traffic distribution through the load balancer, scale-out, scale-in, and the two CloudWatch scaling alarms.

## Outcome
I have a load-balanced web setup that adds and removes servers by itself. I'm still a beginner with Auto Scaling, and I want to keep practicing it. Next is Project 09: Route 53.

## Cost reminder
An ALB charges by the hour while it exists, and the Auto Scaling Group keeps instances running. I delete the Auto Scaling Group first, then the load balancer and the target group, and I check my billing page.
