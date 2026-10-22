# Project 04 — Architecture

```
                     Internet
                        |
                        v
   +------------------------------------------------+
   | Region: us-east-1 (N. Virginia)                |
   |                                                |
   |  +------------------------------------------+  |
   |  | VPC: 04-vpc-network   10.0.0.0/16        |  |
   |  |                                          |  |
   |  |  Internet Gateway                        |  |
   |  |  04-vpc-internet-gateway                 |  |
   |  |           |                              |  |
   |  |           v                              |  |
   |  |  Route table: 04-public-route-table      |  |
   |  |   10.0.0.0/16 -> local                   |  |
   |  |   0.0.0.0/0   -> Internet Gateway        |  |
   |  |           |                              |  |
   |  |           v  (associated with)           |  |
   |  |  +------------------------------------+  |  |
   |  |  | Subnet: 04-public-subnet           |  |  |
   |  |  | 10.0.1.0/24   AZ: us-east-1a       |  |  |
   |  |  | (EC2 and other services can run    |  |  |
   |  |  |  here later)                       |  |  |
   |  |  +------------------------------------+  |  |
   |  +------------------------------------------+  |
   +------------------------------------------------+
```

