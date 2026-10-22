# Project 05 — Learning Notes

## The two layers
```text
VPC
 |
 +-- Subnet  <- Network ACL (guards the subnet boundary)
      |
      +-- EC2 instance  <- Security Group (guards the instance)
```

## Security Group
A firewall attached to the instance. It is **stateful**: if a request is allowed in, the reply is allowed out automatically. It only has allow rules.

## Network ACL (NACL)
A firewall at the subnet boundary. It is **stateless**: I must allow traffic in each direction myself. It has numbered rules, and each rule is Allow or Deny.

## Security Group vs Network ACL
| | Security Group | Network ACL |
|---|---|---|
| Works at | The instance | The subnet |
| State | Stateful | Stateless |
| Rules | Allow only | Allow and Deny |
| Order | All rules checked | Lowest rule number first |

## NACL rule order
Rules are checked from the lowest number to the highest. The first match wins. The `*` rule at the end denies everything that didn't match.

## My NACL (`05-web-network-acl`)
| Direction | Rule | Port | Action |
|---|---|---|---|
| Inbound | 100 | HTTP 80 | Allow |
| Inbound | `*` | All | Deny |
| Outbound | 100 | TCP 1024 - 65535 | Allow |
| Outbound | `*` | All | Deny |

A new custom NACL starts with only the deny-all rules, so nothing gets through until I add allow rules.

## My Security Group (`05-web-security-group`)
- Inbound: HTTP (TCP 80) from `0.0.0.0/0`
- Outbound: all traffic

## Ephemeral ports
Browsers use high ports (1024 - 65535) to receive replies. Because a NACL is stateless, the outbound rule has to allow them, or the replies are blocked.

## Traffic path
```text
Internet -> Public IPv4 -> Network ACL -> Subnet -> Security Group -> EC2 -> Apache -> Browser
```

## Apache on Amazon Linux
The Apache package and service are called `httpd` here.

| Command | What it does |
|---|---|
| `sudo systemctl status httpd` | Shows whether the service is running |
| `sudo systemctl start httpd` | Starts it now |
| `sudo systemctl enable httpd` | Makes it start automatically after a reboot |

## Remember
A NACL that only allows port 80 inbound also blocks other ports, such as SSH (22). I have to plan every port I need, for both the NACL and the Security Group.

## Cost awareness
A running instance and its public IPv4 address can cost money. Stop or terminate the instance when I'm finished, and check Billing.

## Self-test
1. What is the difference between a Security Group and a Network ACL?
2. What does "stateful" mean, and what does "stateless" mean?
3. Why did I need the outbound rule for ports 1024 - 65535?
4. What does a new custom NACL do before I add rules?
5. What is the difference between `systemctl start` and `systemctl enable`?
6. If the website doesn't load, what do I check?

### Answers
1. A Security Group protects the instance and is stateful. A Network ACL protects the subnet and is stateless.
2. Stateful: replies to allowed traffic are allowed automatically. Stateless: each direction needs its own rule.
3. Browsers receive replies on high ports, and a NACL doesn't allow replies automatically.
4. It denies all traffic.
5. `start` runs the service now. `enable` makes it start again after a reboot.
6. Both layers (the NACL and the Security Group), then whether Apache is running and the public IP is right.
