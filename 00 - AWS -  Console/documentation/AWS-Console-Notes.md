# Project 00 — Learning Notes

## Region

A Region is a geographic location where AWS runs multiple Availability Zones.

Examples I saw:

* `us-east-1` (N. Virginia)
* `us-east-2` (Ohio)
* `eu-west-2` (London)

## Availability Zone

An Availability Zone is one or more isolated data centers inside a Region.

```text
US East (N. Virginia) = us-east-1
├── us-east-1a
├── us-east-1b
└── us-east-1c
```

## Billing

The Billing dashboard lets me:

* monitor AWS costs
* check monthly spending
* view AWS Credits
* create Budgets

## AWS Credits

Credits are promotional money that covers eligible services. I check them before creating resources.

## Search bar

The fastest way I found to open a service, for example: EC2, S3, IAM, Lambda.

## Pinned services

IAM · S3 · EC2 · CloudFormation · CloudWatch · Billing · VPC · Aurora \& RDS

## Habits I'm building

* Check the Region before creating anything.
* Check Billing regularly.
* Pin the services I use often.
* Use the search bar instead of scrolling through hundreds of services.

## Self-test

1. What is a Region?
2. What is an Availability Zone?
3. Why check the Region before creating a resource?
4. Why check AWS Credits and Billing?

### Answers

1. A geographic location where AWS runs multiple Availability Zones.
2. One or more isolated data centers inside a Region.
3. Resources are created in the selected Region, and not every service is available in every Region.
4. To avoid surprise charges and to know what my credits cover.

