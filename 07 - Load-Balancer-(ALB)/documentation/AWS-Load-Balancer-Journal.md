# Project 07 — Project Journal

**Date:** September 10–11, 2026

## Goal
Build an internet-facing Application Load Balancer that shares HTTP traffic between two EC2 web servers in different Availability Zones.

## Work completed
1. Created the VPC `07-alb-vpc` (`10.7.0.0/16`), the Internet Gateway `07-internet-gateway`, two public subnets (`10.7.1.0/24` and `10.7.2.0/24`) and a public route table.
2. Created the ALB security group and the web server security group.
3. Launched two web servers (`t3.micro`, Amazon Linux 2023), one in `us-east-1a` and one in `us-east-1b`.
4. Started and enabled Apache (`httpd`) on both, and wrote a different page on each: "Server 1" and "Server 2".
5. Created the target group `07-alb-target-group` (HTTP 80, health check path `/`) with both servers.
6. Created the ALB `07-application-load-balancer` (internet-facing, IPv4, two Availability Zones) with an HTTP :80 listener that forwards to the target group.
7. Opened the ALB address in a browser and troubleshot the timeout.
8. Checked that both targets were Healthy.
9. Opened the ALB address and saw both Server 1 and Server 2 answer.

## What I learned
- An ALB sits between visitors and servers, and the listener decides where requests go.
- The target group holds the servers, and health checks decide which ones get traffic.
- Using two Availability Zones improves availability.
- Visitors should use the ALB's DNS name, not the servers' own IPs.
- The ALB DNS name can resolve to more than one IP address.
- In a real setup, the web server security group should only accept traffic from the ALB security group.

## Issue and lesson
The architecture looked simple (Internet, ALB, Target Group, EC2), but when I first opened the ALB DNS name in Microsoft Edge, the browser timed out. The console looked correct, so I wasn't sure what was wrong.

I didn't rebuild the project. I checked one piece at a time, and each result was PASS:

| # | Check | Result |
|---|---|---|
| 1 | ALB security group allows HTTP 80 | PASS |
| 2 | Correct security group attached to the ALB | PASS |
| 3 | Both ALB subnets route `0.0.0.0/0` to the Internet Gateway | PASS |
| 4 | Network ACL not blocking traffic | PASS |
| 5 | ALB Active, internet-facing, IPv4 | PASS |
| 6 | Listener HTTP :80 forwards to `07-alb-target-group` | PASS |
| 7 | ALB mapped to `us-east-1a` and `us-east-1b` | PASS |
| 8 | `07-internet-gateway` attached to `07-alb-vpc` | PASS |
| 9 | Both servers allow HTTP 80 and pass EC2 status checks | PASS |
| 10 | DNS resolution tested with `nslookup` | Tested |

On Server 2 I also made a small mistake: I reused the Server 1 command and wrote the Server 1 message first, then replaced it with the Server 2 message.

Lesson: when something can't be reached, follow the path in order (client, DNS, internet, Internet Gateway, subnet, security group, listener, target group, target health, server) and don't change settings at random. `nslookup` shows whether DNS works. `curl` shows whether a real connection works. An HTTP `200 OK` shows that the request reached the web server.

## Mistakes to avoid (for my future projects)
- Changing settings at random when something times out.
- Copying a command from one server to the next without reading it.
- Leaving the web server security group open to the whole internet in a real setup.
- Leaving an ALB or instances running when I'm finished.

## Evidence
Screenshots: web server security group, both instances running with status checks passed, Apache setup on Server 1 and Server 2, the ALB details (Active, internet-facing, two Availability Zones), the target group with two Healthy targets, and the browser showing Server 1 and Server 2 through the ALB address.

## Outcome
My ALB shares requests between two servers in two Availability Zones, and both servers show as Healthy. I'm still a beginner with load balancing, and I want to keep practicing it. Next is Project 08: Auto Scaling.

## Cost reminder
An Application Load Balancer charges by the hour while it exists, and the instances cost money while they run. I check my billing page and delete the ALB, the target group and the instances when I no longer need them.
