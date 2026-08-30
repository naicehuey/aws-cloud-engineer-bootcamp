# AWS Project Journal

**Project:** 03 - EC2 Web Server
**Date:** August 2026

---

## Today's Objective

Today I learned how to deploy my first Linux server using Amazon EC2.

The objective was to understand how cloud servers are created, configured, connected, and used to host websites.

Unlike previous projects, this lab introduced Linux administration alongside AWS infrastructure.

---

## What I Built

I launched an Ubuntu EC2 instance on AWS and configured it as a web server.

After connecting through EC2 Instance Connect, I explored the Linux environment, installed Apache2, verified that the web server was running, and hosted a simple HTML website accessible through the instance's public IPv4 address.

---

## Linux Commands Practiced

Today I practiced several basic Linux commands, including:

- whoami
- pwd
- ls
- cd
- uname -a
- cat /etc/os-release

These commands helped me identify the logged-in user, navigate directories, inspect the operating system, and understand the Linux environment running on the EC2 instance.

---

## Apache Web Server

I installed Apache2 using the Ubuntu package manager and verified that the service was running successfully.

I also explored the default Apache web directory and learned where website files are stored on Linux servers.

---

## Networking

This project introduced Security Groups and inbound firewall rules.

I configured:

- SSH (22)
- HTTP (80)
- HTTPS (443)

These rules allow administrators to remotely manage the server while allowing visitors to access hosted websites.

---

## Challenges

One issue I encountered was attempting to open the website using HTTPS before SSL was configured.

After troubleshooting, I accessed the website using HTTP and confirmed that Apache was serving web pages correctly.

This experience reinforced the importance of understanding protocols, ports, and server configuration.

---

## Reflection

This project helped me understand that cloud engineering is not only about AWS services but also about Linux administration, networking, and troubleshooting.

Deploying my first Linux web server gave me practical experience with real cloud infrastructure and increased my confidence working with EC2.

---

## Next Steps

Next, I will continue learning additional AWS services while expanding my Linux knowledge and deploying more realistic cloud projects.