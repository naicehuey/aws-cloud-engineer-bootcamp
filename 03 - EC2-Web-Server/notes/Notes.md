# EC2 Notes

## Amazon EC2

Amazon Elastic Compute Cloud (EC2) is AWS's virtual server service.

Instead of buying physical hardware, users can launch virtual machines on demand.

---

## Instance

An instance is a virtual computer running inside AWS.

Each instance has:

- CPU
- Memory
- Storage
- Operating System
- Network Interface

---

## Amazon Machine Image (AMI)

An AMI is a template used to create EC2 instances.

It contains:

- Operating System
- Default software
- Configuration
- Boot information

Example:

Ubuntu 24.04 LTS

---

## Instance Type

The instance type determines the hardware allocated to the virtual machine.

Example:

t3.micro

It specifies:

- Number of vCPUs
- Memory (RAM)
- Performance characteristics

---

## Security Group

A Security Group acts as a virtual firewall.

It controls which network traffic is allowed to reach an EC2 instance.

---

## Common Ports

### SSH

Port:

22

Purpose:

Secure remote administration of Linux servers.

---

### HTTP

Port:

80

Purpose:

Serves standard web pages over the internet.

---

### HTTPS

Port:

443

Purpose:

Serves encrypted and secure web traffic using SSL/TLS.

---

## Public IPv4 Address

A Public IPv4 address allows users on the internet to connect to an EC2 instance.

It can be used to:

- Open hosted websites
- Connect through SSH
- Access APIs

---

## Apache2

Apache2 is an open-source web server.

It receives HTTP requests from browsers and responds by serving website files.

---

## Apache Web Root

Default directory:

```text
/var/www/html
```

Files placed inside this directory are served to visitors.

Example:

```text
index.html
```

becomes the website's home page.

---

## Basic Linux Commands

```bash
whoami
```

Displays the currently logged-in user.

---

```bash
pwd
```

Displays the current working directory.

---

```bash
ls
```

Lists files and folders in the current directory.

---

```bash
cd
```

Changes the current directory.

---

```bash
uname -a
```

Displays Linux kernel information.

---

```bash
cat /etc/os-release
```

Displays operating system information.

---

## Key Lessons

- EC2 provides virtual servers in the AWS Cloud.
- An AMI is used to create an instance.
- Security Groups control network access.
- Apache hosts websites on Linux.
- Website files are stored in `/var/www/html`.
- HTTP uses port 80.
- HTTPS uses port 443.
- SSH uses port 22.
- Linux command-line skills are essential for cloud engineers.
- Troubleshooting is a normal part of deploying cloud infrastructure.