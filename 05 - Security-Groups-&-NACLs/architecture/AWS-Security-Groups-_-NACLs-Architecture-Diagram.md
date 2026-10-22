# Project 05 — Architecture

```
                    Internet
                       |
                       v
             Public IPv4 address
                       |
                       v
   +----------------------------------------------+
   | Network ACL: 05-web-network-acl              |
   |  Inbound : 100 allow HTTP 80, \* deny         |
   |  Outbound: 100 allow TCP 1024-65535, \* deny  |
   |   (stateless: each direction has its rules)  |
   |                                              |
   |  +----------------------------------------+  |
   |  | Subnet: 05-security\_subnet             |  |
   |  | 172.31.96.0/24   AZ: us-east-1a        |  |
   |  | (default VPC 172.31.0.0/16)            |  |
   |  |                                        |  |
   |  |  +----------------------------------+  |  |
   |  |  | Security Group:                  |  |  |
   |  |  | 05-web-security-group            |  |  |
   |  |  | Inbound : HTTP 80                |  |  |
   |  |  | Outbound: all traffic            |  |  |
   |  |  | (stateful)                       |  |  |
   |  |  |                                  |  |  |
   |  |  |  EC2: 05-web-server              |  |  |
   |  |  |  t3.micro, Amazon Linux 2023     |  |  |
   |  |  |  Apache (httpd)                  |  |  |
   |  |  +----------------------------------+  |  |
   |  +----------------------------------------+  |
   +----------------------------------------------+
                       |
                       v
         Web browser: "It works!"
```

