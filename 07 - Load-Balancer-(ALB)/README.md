# Project 07 — Application Load Balancer

## Overview
My first lab with an Application Load Balancer (ALB). I built my own network, launched two Apache web servers in two different Availability Zones, and put an internet-facing ALB in front of them. The ALB sends visitors to either server through one address, and I can see which server answered because each one shows a different message. When I first opened the ALB address, my browser timed out, so I had to check the setup one piece at a time. I'm a beginner with load balancing, so this README records what I did and what I understood so far.

## Stack
Elastic Load Balancing (ALB) · Amazon EC2 · Amazon VPC · Security Groups · Apache HTTP Server (`httpd`) · Amazon Linux 2023 · AWS Management Console

## What I practiced
- Building a VPC with two public subnets in two Availability Zones
- Launching two EC2 web servers and setting up Apache on each
- Creating a target group with a health check
- Creating an ALB with an HTTP listener
- Using two security groups, one for the ALB and one for the servers
- Troubleshooting a timeout by checking each layer in order

## AWS resources
| Resource | Name | Details |
|---|---|---|
| VPC | `07-alb-vpc` | `10.7.0.0/16` |
| Internet Gateway | `07-internet-gateway` | Attached to `07-alb-vpc` |
| Public subnet 1 | (public subnet in `us-east-1a`) | `10.7.1.0/24` |
| Public subnet 2 | (public subnet in `us-east-1b`) | `10.7.2.0/24` |
| Public route table | (public route table) | `10.7.0.0/16` to `local`, `0.0.0.0/0` to the Internet Gateway |
| ALB security group | `07-alb-security-group` | HTTP 80 from the internet |
| Web server security group | `07-web-server-security-group` | HTTP 80 (open for testing) |
| EC2 web server 1 | `07-alb-web-server-1` | `t3.micro`, Amazon Linux 2023, `us-east-1a` |
| EC2 web server 2 | `07-alb-web-server-2` | `t3.micro`, Amazon Linux 2023, `us-east-1b` |
| Target group | `07-alb-target-group` | Instances, HTTP 80, health check path `/` |
| Load balancer | `07-application-load-balancer` | Application, internet-facing, IPv4, 2 Availability Zones |
| Listener | HTTP :80 | Forwards to `07-alb-target-group` |

## Architecture
```text
Internet
   |
Internet Gateway
   |
Application Load Balancer
   |
HTTP :80 listener
   |
07-alb-target-group
   |-------------------|
   |                   |
EC2 Web Server 1   EC2 Web Server 2
us-east-1a         us-east-1b
   |                   |
Apache             Apache
```

## Web servers
Both servers run Apache (`httpd`). Each one shows a different message so I can tell which server answered:

- Server 1: `Server 1 - Application Load Balancer Project`
- Server 2: `Server 2 - Application Load Balancer Project`

## Security
- The ALB security group allows HTTP (port 80) from the internet.
- The web server security group allows HTTP (port 80) so I could test the servers.
- For a real setup, the web server rule should only allow traffic that comes from the ALB security group, not from anywhere (`0.0.0.0/0`). That stops people from reaching the servers directly.

## Project structure
```text
01 - project/
02 - documentation/
03 - screenshots/
```

## What I did
1. Created the VPC `07-alb-vpc`, the Internet Gateway, two public subnets and a public route table.
2. Created the two security groups.
3. Launched two EC2 web servers, one in each Availability Zone.
4. Connected to each server, started and enabled Apache, and wrote a different page on each one.
5. Created the target group `07-alb-target-group` with the two servers registered.
6. Created the internet-facing ALB across the two Availability Zones, with an HTTP :80 listener that forwards to the target group.
7. Opened the ALB address in a browser. It timed out, so I checked each part of the path (see Challenge).
8. Checked the target group: both servers showed as Healthy.
9. Opened the ALB address again and saw both "Server 1" and "Server 2" served through the same address.
10. Organised the screenshots and wrote this documentation.

## Key ideas (in my own words)
- **Application Load Balancer:** sits between visitors and my servers and shares the requests between them. It works with HTTP and HTTPS (layer 7).
- **Listener:** waits for connections on a port. Mine listens on HTTP :80 and forwards to the target group.
- **Target group:** the group of servers the ALB sends traffic to.
- **Health check:** the ALB checks each server (HTTP, port 80, path `/`). A healthy server gets traffic, and an unhealthy one is left out.
- **Multiple Availability Zones:** if one zone has a problem, the other can keep serving.
- **ALB address:** visitors use the ALB's DNS name, not the servers' own IP addresses.

## Challenge
When I first opened the ALB DNS name, the browser timed out, even though the console looked correct. Instead of rebuilding everything, I checked the path one piece at a time:

1. ALB security group allows HTTP 80
2. The right security group is attached to the ALB
3. Both ALB subnets have `0.0.0.0/0` to the Internet Gateway
4. The network ACL isn't blocking traffic
5. The ALB is Active, internet-facing and IPv4
6. The listener forwards HTTP :80 to `07-alb-target-group`
7. The ALB is mapped to `us-east-1a` and `us-east-1b` (`10.7.1.0/24` and `10.7.2.0/24`)
8. `07-internet-gateway` is attached to `07-alb-vpc`
9. Both servers allow HTTP 80 and pass their EC2 status checks
10. DNS resolution, tested with `nslookup`

None of the first nine checks showed a configuration fault. On the second server I also first wrote the Server 1 message by mistake (I reused the previous command), and then replaced it with the Server 2 message.

Lesson: when something can't be reached, follow the path in order and don't change settings at random. `nslookup` shows whether DNS works, and `curl` shows whether a real connection works.

## Validation checklist
- [x] VPC, Internet Gateway, two public subnets and a public route table created
- [x] Two security groups created
- [x] Two EC2 web servers launched in two Availability Zones
- [x] Apache started and enabled on both servers
- [x] Target group created with two registered targets
- [x] Both targets Healthy
- [x] Internet-facing ALB created with an HTTP :80 listener
- [x] ALB address serves both Server 1 and Server 2
- [x] Screenshots captured (see `03 - screenshots/`)
- [ ] HTTPS (not set up in this project)
- [ ] Web server security group limited to the ALB security group (not done yet)

## Notes
An Application Load Balancer charges by the hour while it exists, and the two instances cost money while they run, so I check my billing page and delete the ALB, the target group and the instances when I'm finished. The site uses plain HTTP. I'm still learning networking and load balancing and want to practice both more.

Documentation was written with AI assistance (Claude) for structure and clarity. I did the lab in the AWS Console myself and checked what is written here against what I did.
