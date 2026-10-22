# Project 03 — EC2 Web Server

## Overview
My first Linux server on AWS. I launched an Ubuntu server with Amazon EC2, connected to it from the browser with EC2 Instance Connect, installed the Apache2 web server, and used it to host a simple HTML page that I opened through the server's public IPv4 address. This was also my first time practicing Linux commands together with AWS. I'm a beginner with EC2 and Linux, so this README records what I did and what I understood so far.

## Stack
Amazon EC2 · Ubuntu Server 24.04 LTS · Apache2 · Linux · HTML · AWS Management Console

## What I practiced
- Launching an EC2 instance
- Choosing an AMI and an instance type
- Setting up a Security Group (SSH, HTTP and HTTPS rules)
- Connecting to a Linux server with EC2 Instance Connect
- Basic Linux commands
- Installing and checking Apache2
- Finding the Apache web root and replacing the default page
- Opening the site through the public IPv4 address

## Instance configuration
| Setting | Value |
|---|---|
| Operating system | Ubuntu Server 24.04 LTS |
| Instance type | t3.micro |
| Storage | 8 GB gp3 |
| Connection method | EC2 Instance Connect |
| Web server | Apache2 |

## Security group rules
| Type | Port | Why |
|---|---|---|
| SSH | TCP 22 | Remote administration |
| HTTP | TCP 80 | Website access |
| HTTPS | TCP 443 | Secure web traffic (SSL was not set up yet) |

## Project structure
```text
01 - project/
02 - documentation/
03 - screenshots/
```

## Linux commands I practiced
```bash
whoami
pwd
ls
cd
uname -a
cat /etc/os-release
sudo apt update
sudo apt install apache2
sudo systemctl status apache2
apache2 -v
```

## What I did
1. Launched an Ubuntu EC2 instance.
2. Set up networking and the security group.
3. Connected using EC2 Instance Connect.
4. Explored the Linux environment.
5. Checked the current user and working directory.
6. Checked the Ubuntu version.
7. Installed Apache2.
8. Checked that Apache was running and which version it was.
9. Explored the Apache web directory.
10. Opened the default Apache page using the public IPv4 address.
11. Replaced the default page with my own HTML page.
12. Organised the screenshots and wrote this documentation.

## Key ideas (in my own words)
- **EC2 instance:** a virtual computer running in AWS.
- **AMI:** the template used to create an instance (the operating system and starting software).
- **Instance type:** decides the CPU and memory. Mine was `t3.micro`.
- **Security group:** a virtual firewall that decides which traffic can reach the instance.
- **Apache2:** a web server that answers browser requests with website files.
- **Web root:** `/var/www/html`. Files placed there are served to visitors, and `index.html` becomes the home page.
- **Public IPv4 address:** the address visitors use to reach the instance from the internet.

## Challenge
I tried to open the website with HTTPS before any SSL certificate was set up, and it didn't work. After checking, I opened it with HTTP and saw that Apache was serving the page correctly. The lesson for me: opening port 443 isn't enough. HTTPS also needs a certificate, and the server has to be set up for it.

## Validation checklist
- [x] Ubuntu EC2 instance launched
- [x] Security group set up (SSH, HTTP, HTTPS)
- [x] Connected with EC2 Instance Connect
- [x] Linux commands practiced
- [x] Apache2 installed and running
- [x] Website opened through the public IPv4 address
- [x] Default page replaced with a custom HTML page
- [x] Screenshots captured (see `03 - screenshots/`)
- [ ] HTTPS with an SSL certificate (not done yet)

## Notes
The instance and its public IPv4 address can cost money while they exist, so I check my billing page and stop or terminate the instance when I'm finished. I'm still learning Linux and networking and want to practice more of both in the projects ahead.

Documentation was written with AI assistance (Claude) for structure and clarity. I did the lab in the AWS Console myself and checked what is written here against what I did.
