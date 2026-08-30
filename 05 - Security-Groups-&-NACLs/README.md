# Project 05 — Web Server Security & Network ACLs

## Overview

This project demonstrates how network-level and instance-level security controls work together in AWS.

I created a web server environment using Amazon EC2 and configured:

- A VPC
- A custom subnet
- A Security Group
- A custom Network ACL
- Inbound and outbound NACL rules
- EC2 Instance Connect
- Apache HTTP Server
- HTTP access from the Internet

The main goal of this project was to understand the difference between a Security Group and a Network ACL and how network traffic travels through an AWS environment.

---

## Architecture

```text
                    Internet
                       |
                       v
                Public IPv4 Address
                       |
                       v
              Network ACL (NACL)
                       |
                       v
                    Subnet
                       |
                       v
              Security Group
                       |
                       v
                    EC2
                       |
                       v
                  Apache HTTP
                       |
                       v
                 Web Browser