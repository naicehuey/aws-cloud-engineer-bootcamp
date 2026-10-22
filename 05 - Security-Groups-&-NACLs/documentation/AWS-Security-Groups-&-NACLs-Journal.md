# Project 05 — Project Journal

**Date:** August 18, 2026

## Goal
Learn how AWS protects a web server with two layers, a Security Group and a Network ACL, and see how traffic travels through them.

## Work completed
1. Created the subnet `05-security_subnet` (`172.31.96.0/24`) in `us-east-1a`, in my default VPC.
2. Created the Security Group `05-web-security-group` with an inbound HTTP rule (port 80) and the default outbound rule.
3. Created the custom Network ACL `05-web-network-acl`.
4. Added NACL rule 100 inbound: allow HTTP (80). Added NACL rule 100 outbound: allow TCP 1024 - 65535.
5. Associated the Network ACL with `05-security_subnet`.
6. Launched `05-web-server` (`t3.micro`, Amazon Linux 2023) in the subnet, with auto-assign public IP and my Security Group.
7. Confirmed the instance was running with 3/3 status checks passed.
8. Connected in the browser and installed Apache (`httpd`).
9. Started and enabled Apache with `systemctl`.
10. Opened the public IP in a browser and saw "It works!".

## What I learned
- A Security Group works at the instance and is stateful. A Network ACL works at the subnet and is stateless.
- A new custom Network ACL denies everything until I add allow rules.
- NACL rules are checked from the lowest number up, and the `*` rule denies whatever is left.
- Because a NACL is stateless, I had to allow the reply traffic (ports 1024 - 65535) on the way out.
- `systemctl start` runs a service now, and `systemctl enable` makes it start again after a reboot.

## Issue and lesson
This project was harder than my earlier ones, and the challenge was networking. At first I understood the setup mainly as console settings, and I couldn't yet explain what was happening to the traffic. Writing the NACL rules myself, and seeing that a new NACL starts with a deny-all rule, helped me understand it.

Lesson: understand the traffic path first, then create the rules. When something doesn't load, check both layers, the Network ACL and the Security Group.

I also saw that Apache was installed but "inactive (dead)" and "disabled" at first. I started it, and then enabled it so it survives a reboot.

## Mistakes to avoid (for my future projects)
- Forgetting the outbound rule for reply traffic on a NACL.
- Forgetting that a NACL that only allows port 80 also blocks other ports, such as SSH (22).
- Checking only the Security Group when something doesn't load.
- Leaving an instance running when I'm finished.

## Evidence
Screenshots: Security Group inbound and outbound rules, Network ACL creation, NACL inbound rules before and after adding the allow rule, NACL outbound rules, subnet creation, subnet and NACL association, instance launch settings, running instance with status checks, Apache installation and `systemctl` output, and the browser showing "It works!".

## Outcome
I have a web server behind a Network ACL and a Security Group, and I can explain how they differ. I'm still a beginner with networking, and I want to keep practicing it. Next is Project 06: EBS storage.

## Cost reminder
A running instance and its public IPv4 address can cost money. I check my billing page and stop or terminate the instance when I no longer need it.
