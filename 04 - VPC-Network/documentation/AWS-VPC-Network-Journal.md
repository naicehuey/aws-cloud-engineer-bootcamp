# Project 04 — Project Journal

**Date:** August 2026

## Goal
Build a basic AWS network from scratch and understand how traffic moves through it. This was my first lab focused only on VPC networking, and the aim was to understand the pieces, not just click through creating them.

## Work completed
1. Created the VPC `04-vpc-network` with the CIDR block `10.0.0.0/16` in `us-east-1`.
2. Created the subnet `04-public-subnet` (`10.0.1.0/24`) in the Availability Zone `us-east-1a`.
3. Created the Internet Gateway `04-vpc-internet-gateway` and attached it to the VPC.
4. Created the route table `04-public-route-table`.
5. Added a default route (`0.0.0.0/0`) to the Internet Gateway.
6. Associated the route table with `04-public-subnet`.
7. Checked the routes: `10.0.0.0/16` to `local`, and `0.0.0.0/0` to the Internet Gateway.

## What I learned
- A VPC is my own network inside AWS, and a subnet is a slice of it in one Availability Zone.
- An Internet Gateway has to be created and attached before the VPC can reach the internet.
- The route table decides where traffic goes. A subnet is only "public" if its route table has a route to an Internet Gateway.
- The `local` route is added automatically and keeps traffic inside the VPC.
- AWS reserves 5 addresses in every subnet, so a `/24` gives 251 usable addresses.
- A VPC is the network that other AWS services, like EC2, run inside.

## Mistakes to avoid (for my future projects)
- Forgetting to attach the Internet Gateway to the VPC.
- Creating the route but forgetting to associate the route table with the subnet.
- Picking CIDR ranges that overlap with other networks.
- Assuming a subnet is public just because I named it "public".

## Evidence
Screenshots: VPC details and resource map, Internet Gateway attached to the VPC, subnet created, and the subnet's route table with its routes.

## Outcome
I now have a custom VPC with a public subnet that has a route to the internet. I'm still a beginner with networking, and I want to keep practicing it. A small note for myself: the Internet Gateway's Name tag value shows as "Name tag: 04-vpc-internet-gateway", so the word "Name tag:" ended up inside the value and I can fix it under Manage tags. Next is Project 05: Security Groups and Network ACLs.

## Cost reminder
The VPC, subnet, route table and Internet Gateway have no extra charge. NAT gateways, Elastic IPs and public IPv4 addresses can cost money, so I check my billing page and delete resources I no longer need.
