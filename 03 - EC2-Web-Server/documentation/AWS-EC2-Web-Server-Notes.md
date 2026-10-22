# Project 03 — Learning Notes

## Amazon EC2
Amazon Elastic Compute Cloud (EC2) is AWS's virtual server service. Instead of buying physical hardware, I can launch virtual machines when I need them.

## Instance
A virtual computer running inside AWS. Each instance has CPU, memory, storage, an operating system and a network interface.

## Amazon Machine Image (AMI)
A template used to create an instance. It contains the operating system, default software, configuration and boot information. Mine: Ubuntu 24.04 LTS.

## Instance type
Decides the hardware: number of vCPUs, memory (RAM) and performance. Mine: `t3.micro`.

## Security group
A virtual firewall. It controls which network traffic can reach the instance.

## Common ports
| Name | Port | Purpose |
|---|---|---|
| SSH | 22 | Secure remote administration of Linux servers |
| HTTP | 80 | Serves normal web pages |
| HTTPS | 443 | Serves encrypted web traffic using SSL/TLS |

Best practice: only open the ports I need, and limit who can reach port 22.

## Public IPv4 address
Lets people on the internet reach the instance. It can be used to open websites, connect with SSH and reach APIs. It can also cost a small amount while it exists.

## Apache2
An open-source web server. It receives HTTP requests from browsers and answers with website files.

## Apache web root
```text
/var/www/html
```
Files placed here are served to visitors. `index.html` becomes the home page.

## Linux commands
| Command | What it does |
|---|---|
| `whoami` | Shows the current user |
| `pwd` | Shows the current directory |
| `ls` | Lists files and folders |
| `cd` | Changes directory |
| `uname -a` | Shows kernel information |
| `cat /etc/os-release` | Shows operating system information |
| `sudo apt update` | Refreshes the list of available packages |
| `sudo apt install apache2` | Installs Apache2 |
| `sudo systemctl status apache2` | Shows whether Apache is running |
| `apache2 -v` | Shows the Apache version |

## HTTP vs HTTPS
My site worked over HTTP. HTTPS failed because no SSL certificate was set up. Opening port 443 in the security group only allows the traffic in. The server still needs a certificate to answer it.

## Cost awareness
A running instance and its public IPv4 address can cost money. Stop or terminate the instance when I'm finished, and check Billing.

## Key lessons
- EC2 gives me virtual servers in the AWS Cloud.
- An AMI is used to create an instance.
- Security groups control network access.
- Apache hosts websites on Linux, and website files go in `/var/www/html`.
- HTTP is port 80, HTTPS is port 443 and SSH is port 22.
- Linux command-line skills are useful for cloud work.
- Troubleshooting is a normal part of deploying cloud infrastructure.

## Self-test
1. What is an AMI?
2. What does a security group do?
3. Which ports did I open, and what is each for?
4. Where does Apache serve website files from?
5. Why did HTTPS fail on my server?
6. What can cost money while the instance exists?

### Answers
1. A template used to create an instance, with the operating system and starting software.
2. It works as a firewall and decides which traffic can reach the instance.
3. 22 for SSH (managing the server), 80 for HTTP (web pages) and 443 for HTTPS (secure web traffic).
4. `/var/www/html`.
5. No SSL certificate was set up. An open port 443 isn't enough on its own.
6. The running instance, its storage and its public IPv4 address.
