# Project 04 — Learning Notes

## What is a VPC?
VPC stands for Virtual Private Cloud. It is a logically isolated virtual network in AWS where I can run AWS resources. It is the base for subnets, route tables and network security controls.

## VPC CIDR
A VPC needs an IP address range. For this project I used:

```text
10.0.0.0/16
```

## Subnet
A subnet is a smaller range inside the VPC, placed in one Availability Zone.

```text
VPC 04-vpc-network  10.0.0.0/16
└── Subnet 04-public-subnet  10.0.1.0/24  (us-east-1a)
```

AWS reserves 5 addresses in every subnet. A `/24` has 256 addresses, so 251 are available.

## Availability Zone
One or more isolated data centers inside a Region. My subnet is in `us-east-1a`.

## Internet Gateway
Connects the VPC to the internet. It must be attached to the VPC. Mine: `04-vpc-internet-gateway`.

## Route table and routes
A route table is a set of rules for where traffic goes. Mine: `04-public-route-table`.

| Destination | Target | Meaning |
|---|---|---|
| `10.0.0.0/16` | `local` | Stay inside the VPC |
| `0.0.0.0/0` | Internet Gateway | Everything else goes to the internet |

`0.0.0.0/0` is the default route and means "any address".

## Route table association
A route table does nothing for a subnet until it is associated with it. I associated `04-public-route-table` with `04-public-subnet`.

## Public subnet
A subnet whose route table has a route to an Internet Gateway. The name alone doesn't make it public.

## Auto-assign public IPv4
My subnet has this set to "No". A server launched there would need a public IP set up separately.

## How the pieces fit
```text
Internet <-> Internet Gateway <-> Route table <-> Subnet <-> (EC2 and other resources)
```

## Cost awareness
The VPC, subnet, route table and Internet Gateway have no extra charge. NAT gateways, Elastic IPs and public IPv4 addresses can cost money.

## Self-test
1. What is a VPC?
2. What does `10.0.0.0/16` mean here?
3. Why does my `/24` subnet show 251 available addresses?
4. What does an Internet Gateway do?
5. What does the route `0.0.0.0/0` to the Internet Gateway do?
6. What makes a subnet public?
7. Why is the route table association needed?

### Answers
1. My own isolated virtual network inside AWS.
2. The IP address range of the whole VPC.
3. A `/24` has 256 addresses, and AWS reserves 5 of them.
4. It connects the VPC to the internet.
5. It sends all traffic that isn't for the VPC out to the internet.
6. A route in its route table that points to an Internet Gateway.
7. Without it, the subnet doesn't use that route table's rules.
