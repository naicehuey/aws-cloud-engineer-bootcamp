# 03 - EC2 Web Server

## Overview

This project demonstrates the deployment of a Linux web server using Amazon Elastic Compute Cloud (Amazon EC2).

An Ubuntu EC2 instance was launched, configured with Apache2, connected through EC2 Instance Connect, and used to host a simple static website. During the lab, I also practiced basic Linux commands, verified server health, and learned how web servers deliver content over the internet.

This project was completed as part of my AWS Cloud Engineer Bootcamp.

---

## Objectives

The objectives of this project were to:

- Understand the purpose of Amazon EC2.
- Launch an Ubuntu EC2 instance.
- Understand Amazon Machine Images (AMIs).
- Select an appropriate instance type.
- Configure a Security Group.
- Allow SSH, HTTP, and HTTPS traffic.
- Connect to a Linux server using EC2 Instance Connect.
- Learn basic Linux navigation commands.
- Install and verify the Apache2 web server.
- Understand the Apache web root directory.
- Deploy a simple HTML website.
- Access the website through the instance's public IPv4 address.
- Document the deployment process.

---

## AWS Service Used

### Amazon EC2

Amazon Elastic Compute Cloud (EC2) is a service that provides secure, resizable virtual servers in the AWS Cloud.

It allows users to launch Linux or Windows servers on demand and host applications, websites, databases, APIs, and other cloud workloads.

---

## Technologies Used

- Amazon EC2
- Ubuntu Server 24.04 LTS
- Apache2
- Linux
- HTML

---

## Instance Configuration

- Operating System: Ubuntu Server 24.04 LTS
- Instance Type: t3.micro
- Storage: 8 GB gp3
- Authentication: EC2 Instance Connect
- Web Server: Apache2

---

## Security Group Configuration

The instance firewall was configured with the following inbound rules:

- SSH (TCP Port 22) – Remote administration
- HTTP (TCP Port 80) – Website access
- HTTPS (TCP Port 443) – Secure web traffic

These rules allow administrators to manage the server and users to access hosted websites.

---

## Linux Commands Practiced

During this project I practiced:

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

---

## Practical Work

The following activities were completed:

1. Launched an Ubuntu EC2 instance.
2. Configured networking and security groups.
3. Connected using EC2 Instance Connect.
4. Explored the Linux environment.
5. Verified the current user and working directory.
6. Checked Ubuntu version information.
7. Installed Apache2.
8. Verified that Apache was running.
9. Verified the Apache version.
10. Explored the Apache web directory.
11. Tested the web server using the public IPv4 address.
12. Replaced the default website with a custom HTML page.

---

## Screenshots

The project includes screenshots covering:

- EC2 Dashboard
- Launch Configuration
- Successful Launch
- Running Instance
- Status Checks
- Linux Login
- Apache Installation
- Apache Running
- Web Directory
- Default Apache Website
- Custom Website Deployment

---

## Skills Learned

- Amazon EC2
- Linux Fundamentals
- Apache Web Server
- Security Groups
- Public IPv4 Address
- Ubuntu Server Administration
- Cloud Infrastructure
- Web Hosting

---

## Outcome

Successfully deployed a Linux web server on AWS, connected through the browser, installed Apache, explored the Linux environment, and hosted a custom static website accessible through the instance's public IP address.