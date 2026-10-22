# Project 05 — Security Groups & Network ACLs

## Overview
My first lab on network security in AWS. I built a small web server setup and used two different layers of protection: a Security Group on the server and a Network ACL on the subnet. I created a custom subnet and a custom Network ACL, wrote the rules myself, launched an EC2 instance with Apache, and opened the site in a browser over HTTP. The main goal was to understand the difference between a Security Group and a Network ACL and how traffic travels through them. This was harder than my earlier projects, because I had to understand what was really happening to the traffic and not only follow the console settings. I'm a beginner with AWS networking, so this README records what I did and what I understood so far.

## Stack
Amazon VPC · Security Groups · Network ACLs · Amazon EC2 · Amazon Linux 2023 · Apache HTTP Server (`httpd`) · AWS Management Console

## What I practiced
- Creating a custom subnet
- Creating a Security Group with an inbound HTTP rule
- Creating a custom Network ACL and writing its inbound and outbound rules
- Associating the Network ACL with my subnet
- Launching an EC2 instance in that subnet with the Security Group
- Installing, starting and enabling Apache on Linux
- Opening the website from a browser

## Configuration
| Resource | Name | Details |
|---|---|---|
| VPC | default VPC | `172.31.0.0/16` (I used the default VPC for this project) |
| Subnet | `05-security_subnet` | `172.31.96.0/24`, Availability Zone `us-east-1a`, 251 available IPv4 addresses |
| Network ACL | `05-web-network-acl` | Custom (not the default), associated with `05-security_subnet` |
| Security Group | `05-web-security-group` | "Security group for Project 05 web server" |
| EC2 instance | `05-web-server` | `t3.micro`, Amazon Linux 2023, 8 GiB storage, auto-assigned public IP |

### Network ACL rules (`05-web-network-acl`)
| Direction | Rule | Type | Protocol | Port range | Source / Destination | Action |
|---|---|---|---|---|---|---|
| Inbound | 100 | HTTP | TCP (6) | 80 | `0.0.0.0/0` | Allow |
| Inbound | `*` | All traffic | All | All | `0.0.0.0/0` | Deny |
| Outbound | 100 | Custom TCP | TCP (6) | 1024 - 65535 | `0.0.0.0/0` | Allow |
| Outbound | `*` | All traffic | All | All | `0.0.0.0/0` | Deny |

### Security Group rules (`05-web-security-group`)
| Direction | Type | Protocol | Port range | Source / Destination |
|---|---|---|---|---|
| Inbound | HTTP | TCP | 80 | `0.0.0.0/0` |
| Outbound | All traffic | All | All | `0.0.0.0/0` |

## How the traffic flows
```text
Internet -> Public IPv4 address -> Network ACL -> Subnet -> Security Group -> EC2 -> Apache -> Web browser
```

## Project structure
```text
01 - project/
02 - documentation/
03 - screenshots/
```

## What I did
1. Created the subnet `05-security_subnet` in `us-east-1a`.
2. Created the Security Group `05-web-security-group` and allowed inbound HTTP (port 80).
3. Created the custom Network ACL `05-web-network-acl`. A new Network ACL starts with only a deny-all rule, so nothing could get through yet.
4. Added the inbound rule 100 to allow HTTP (port 80).
5. Added the outbound rule 100 to allow TCP ports 1024 to 65535, so the server's replies can go back out.
6. Associated the Network ACL with `05-security_subnet`.
7. Launched the EC2 instance `05-web-server` (`t3.micro`, Amazon Linux 2023) in that subnet, with auto-assign public IP turned on and my Security Group attached.
8. Checked that the instance was running and passed 3/3 status checks.
9. Connected to the instance in the browser and installed Apache (`httpd`).
10. Checked Apache with `sudo systemctl status httpd` (it was inactive), started it with `sudo systemctl start httpd`, and enabled it with `sudo systemctl enable httpd` so it starts again after a reboot.
11. Opened the instance's public IP address in a browser and saw the page "It works!".
12. Organised the screenshots and wrote this documentation.

## Key ideas (in my own words)
- **Security Group:** a firewall attached to the instance. It is stateful, so if a request is allowed in, the reply is allowed out automatically.
- **Network ACL (NACL):** a firewall at the subnet boundary. It is stateless, so I have to allow the traffic in both directions myself.
- **Rule numbers:** a NACL checks its rules from the lowest number up. The `*` rule at the end is the default that denies everything else.
- **Ephemeral ports (1024 - 65535):** the high ports a browser uses to receive replies. Because a NACL is stateless, my outbound rule had to allow them.
- **Two layers:** traffic has to pass the Network ACL for the subnet and the Security Group for the instance.

## Challenge
At first I understood the setup as a list of console settings, and I couldn't yet explain what was happening to the traffic. What helped was seeing that a new custom NACL starts with a deny-all rule, so I needed an inbound allow rule for port 80 and an outbound allow rule for the reply traffic. Writing the rules and seeing the page load made the difference between the Security Group (stateful) and the NACL (stateless) much clearer.

## Validation checklist
- [x] Custom subnet created
- [x] Security Group created with an inbound HTTP rule
- [x] Custom Network ACL created
- [x] Inbound and outbound NACL rules added
- [x] Network ACL associated with the subnet
- [x] EC2 instance launched in the subnet with the Security Group
- [x] Apache installed, started and enabled
- [x] Website opened over HTTP ("It works!")
- [x] Screenshots captured (see `03 - screenshots/`)
- [ ] HTTPS (not set up in this project)

## Notes
A running instance and its public IPv4 address can cost money, so I check my billing page and stop or terminate the instance when I'm finished. My NACL only allows port 80 inbound, so it would also block remote access on other ports (such as SSH on port 22), and I need to remember that when I plan how to manage a server. The site uses plain HTTP, not HTTPS. I'm still learning networking and want to keep practicing it.

Documentation was written with AI assistance (Claude) for structure and clarity. I did the lab in the AWS Console myself and checked what is written here against what I did.
