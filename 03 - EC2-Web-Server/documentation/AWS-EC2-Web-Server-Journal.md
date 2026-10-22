# Project 03 — Project Journal

**Date:** August 2026

## Goal
Launch my first Linux server on AWS, connect to it, and use it to host a website. I wanted to understand how cloud servers are created, connected to and used, and this was my first lab that mixed Linux with AWS.

## Work completed
1. Launched an Ubuntu Server 24.04 LTS instance (`t3.micro`, 8 GB gp3).
2. Set up a security group with SSH (22), HTTP (80) and HTTPS (443) rules.
3. Connected to the server with EC2 Instance Connect.
4. Practiced Linux commands: `whoami`, `pwd`, `ls`, `cd`, `uname -a` and `cat /etc/os-release`.
5. Installed Apache2 with `sudo apt update` and `sudo apt install apache2`.
6. Checked Apache with `sudo systemctl status apache2` and `apache2 -v`.
7. Explored the Apache web directory.
8. Opened the default Apache page using the public IPv4 address.
9. Replaced the default page with my own HTML page.

## What I learned
- An instance is a virtual computer, and an AMI is the template it starts from.
- A security group decides which ports the outside world can reach.
- SSH (22) is for managing the server, HTTP (80) is for web pages and HTTPS (443) is for secure web traffic.
- Apache serves the files in `/var/www/html`.
- The commands I practiced showed me who I was logged in as, where I was, and what system I was on.
- Cloud engineering also needs Linux, networking and troubleshooting, not only AWS services.

## Issue and lesson
I tried to open the website with HTTPS before SSL was set up, and it didn't work. After troubleshooting, I used HTTP and confirmed that Apache was serving the page.

Lesson: ports, protocols and server configuration have to match. Opening port 443 doesn't give me HTTPS by itself, because I also need a certificate.

## Mistakes to avoid (for my future projects)
- Using HTTPS before a certificate is set up.
- Opening ports I don't need.
- Leaving an instance running when I'm finished with it.
- Forgetting that a public IPv4 address can cost money.

## Evidence
Screenshots: EC2 dashboard, launch configuration, successful launch, running instance, status checks, Linux login, Apache installation, Apache running, web directory, default Apache page and custom website.

## Outcome
I now have a Linux web server running on EC2 that serves my own HTML page. I'm still a beginner with Linux and networking, and I want to keep practicing both. Next is Project 04: building a VPC network.

## Cost reminder
A running instance and its public IPv4 address can cost money. I check my billing page and stop or terminate the instance when I no longer need it.
