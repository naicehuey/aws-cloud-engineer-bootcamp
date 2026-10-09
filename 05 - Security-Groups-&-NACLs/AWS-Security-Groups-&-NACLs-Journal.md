
---

# `journal.md`

```markdown
# Project 05 Journal — Web Server Security & Network ACLs

## Day 1 — Building the Security Layer

This project was significantly harder than my previous AWS projects.

The main challenge was networking.

I created a custom Security Group and Network ACL and started learning how AWS evaluates network traffic.

At first, I understood the configuration mainly as a collection of AWS console settings. I was not yet comfortable explaining what was actually happening to the traffic.

The important concept was:

```text
VPC
 ↓
Subnet
 ↓
NACL
 ↓
EC2
 ↓
Security Group