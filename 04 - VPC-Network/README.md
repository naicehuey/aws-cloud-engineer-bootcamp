# Project 04 — VPC Network

## Overview
My first hands-on lab with Amazon VPC networking. I created my own Virtual Private Cloud, added a subnet, created an Internet Gateway and attached it, then built a route table with a route to the internet and connected it to the subnet. The goal was to see how these pieces work together and to understand how a VPC is the network that other AWS services, such as EC2, run inside. I'm a beginner with networking in AWS, so this README records what I did and what I understood so far.

## Stack
Amazon VPC · AWS Management Console

## What I practiced
- Creating a custom VPC with an IPv4 CIDR block
- Creating a subnet in one Availability Zone
- Creating an Internet Gateway and attaching it to the VPC
- Creating a route table and a default route to the internet
- Associating the route table with a subnet
- Reading how a VPC, subnet, route table and Internet Gateway connect

## Network configuration
| Resource | Name | Details |
|---|---|---|
| Region | N. Virginia | `us-east-1` |
| VPC | `04-vpc-network` | IPv4 CIDR `10.0.0.0/16` |
| Subnet | `04-public-subnet` | IPv4 CIDR `10.0.1.0/24`, Availability Zone `us-east-1a`, 251 available IPv4 addresses |
| Internet Gateway | `04-vpc-internet-gateway` | Attached to `04-vpc-network` |
| Route table | `04-public-route-table` | Associated with `04-public-subnet` |

Routes in `04-public-route-table`:

| Destination | Target | Meaning |
|---|---|---|
| `10.0.0.0/16` | `local` | Traffic inside the VPC stays inside the VPC |
| `0.0.0.0/0` | Internet Gateway | All other traffic goes out to the internet |

Other VPC settings I noticed: DNS resolution is enabled, DNS hostnames are disabled, and auto-assign public IPv4 on the subnet is set to "No".

## Project structure
```text
01 - project/
02 - documentation/
03 - screenshots/
```

## What I did
1. Created the VPC `04-vpc-network` with the CIDR block `10.0.0.0/16`.
2. Created the subnet `04-public-subnet` (`10.0.1.0/24`) in `us-east-1a`.
3. Created the Internet Gateway `04-vpc-internet-gateway`.
4. Attached the Internet Gateway to the VPC.
5. Created the route table `04-public-route-table` in the VPC.
6. Added a default route (`0.0.0.0/0`) that points to the Internet Gateway.
7. Associated the route table with `04-public-subnet`.
8. Checked the subnet's Route table tab to confirm the routes.
9. Organised the screenshots and wrote this documentation.

## Key ideas (in my own words)
- **VPC:** my own private network inside AWS. Resources I launch can live inside it.
- **CIDR block:** the range of IP addresses for the network. `10.0.0.0/16` gives the VPC a large range, and the subnet takes a smaller piece (`10.0.1.0/24`) of it.
- **Subnet:** a slice of the VPC's IP range, placed in one Availability Zone. AWS keeps 5 addresses in each subnet for itself, so my `/24` shows 251 available addresses.
- **Internet Gateway:** the door between the VPC and the internet. It has to be attached to the VPC.
- **Route table:** a set of rules that says where network traffic goes.
- **Route:** one rule. The `local` route keeps traffic inside the VPC. The `0.0.0.0/0` route sends everything else to the Internet Gateway.
- **Public subnet:** a subnet whose route table has a route to an Internet Gateway. That route is what makes my subnet "public".

## Validation checklist
- [x] Custom VPC created (`10.0.0.0/16`)
- [x] Subnet created in `us-east-1a` (`10.0.1.0/24`)
- [x] Internet Gateway created and attached to the VPC
- [x] Route table created
- [x] Default route (`0.0.0.0/0`) points to the Internet Gateway
- [x] Route table associated with the subnet
- [x] Routes checked on the subnet's Route table tab
- [x] Screenshots captured (see `03 - screenshots/`)

## Notes
The VPC, subnet, route table and Internet Gateway don't have an extra charge. Things like NAT gateways, Elastic IPs and public IPv4 addresses can cost money, and I didn't create those in this project. The subnet's "auto-assign public IPv4" setting is "No", so a server launched there would need a public IP set up separately. I'm still learning networking and want to practice private subnets and security next.

Documentation was written with AI assistance (Claude) for structure and clarity. I did the lab in the AWS Console myself and checked what is written here against what I did.
