# Project 09 — Route 53 Automated Failover

## Overview
A small DNS failover project. Route 53 normally sends visitors to a web server on EC2 (the primary). A Route 53 health check watches that server. If the server stops answering, Route 53 starts sending visitors to a backup page hosted on S3 instead. I'm still learning DNS and Route 53, so this README records the plan I followed and what I have evidence for so far.

> **Status:** the S3 backup page is built. The EC2, health check, failover records and outage test sections are marked "to confirm" until I add my screenshots and results.

## Stack
Amazon Route 53 (hosted zone, health check, failover records) · Amazon EC2 (Amazon Linux 2023, Apache) · Amazon S3 static website · AWS Management Console

## What I practiced
- Hosting a backup page on S3 static website hosting
- Installing a web server on EC2 with User Data
- Creating a Route 53 health check
- Using the Failover routing policy (Primary and Secondary records)
- Simulating an outage by stopping the instance

## Configuration (plan)
| Item | Value |
|---|---|
| Secondary (backup) | S3 static website, `index.html` |
| Primary | EC2 `Primary-Web-Server`, Amazon Linux 2023, `t3.micro`, Apache |
| Health check | `Primary-EC2-HealthCheck`, HTTP, port 80, path `/`, by IP address |
| Primary record | Type A, TTL 60, Failover = Primary, ID `Primary-EC2-Record` |
| Secondary record | Type A, alias to the S3 website endpoint, Failover = Secondary, ID `Secondary-S3-Record` |
| Domain / hosted zone | Not recorded yet |

## Project structure
```text
09-route53/
├── project/
│   ├── index.html          # my S3 backup page
│   ├── user-data.sh        # EC2 User Data (from the lab plan)
│   └── bucket-policy.json  # public-read policy (replace YOUR-BUCKET-NAME)
├── documentation/
│   ├── Route53-Journal.md
│   └── Route53-Notes.md
├── architecture/
│   └── Route53-Architecture-Diagram.md
├── screenshots/
│   ├── 01-s3-backup-endpoint.png
│   ├── 02-primary-ec2-active.png
│   ├── 03-route53-healthcheck-healthy.png
│   ├── 04-route53-failover-records.png
│   └── 05-failover-traffic-verified.png
└── README.md
```

## Architecture
```text
        Browser
           |
           v
   +----------------+
   |   Route 53     |   Health check watches EC2 (HTTP :80 /)
   +-------+--------+
           |
   +-------+---------------+
   |                       |
Healthy -> Primary     Unhealthy -> Secondary
   |                       |
   v                       v
+---------+          +-------------+
|  EC2    |          |  S3 website |
| Apache  |          |  backup page|
+---------+          +-------------+
```

## Screenshots
Add these once they are captured and hidden where needed (account IDs, public IPs):

1. `01-s3-backup-endpoint.png` — S3 backup page in the browser
2. `02-primary-ec2-active.png` — primary page from EC2
3. `03-route53-healthcheck-healthy.png` — health check shows Healthy
4. `04-route53-failover-records.png` — Primary and Secondary records
5. `05-failover-traffic-verified.png` — backup page served after the outage

## What I did
1. **Backup page (done):** built `index.html` for the S3 bucket. It's a styled "Error 500 / Internal server error" page with a green card saying the S3 failover site is online.
2. **Primary server (to confirm):** launch `Primary-Web-Server` with the User Data script in `project/`.
3. **Hosted zone (to confirm):** create a public hosted zone for a domain I control.
4. **Health check (to confirm):** create `Primary-EC2-HealthCheck` against the EC2 public IP.
5. **Failover records (to confirm):** create the Primary and Secondary records with the same name.
6. **Outage test (to confirm):** stop the instance, wait for Unhealthy, then open the domain.
7. **Clean up (to confirm):** terminate EC2, delete the health check, empty and delete the bucket, delete the hosted zone if not needed.

## Key ideas (in my own words)
- **Route 53** answers DNS questions. It doesn't restart or fix my server.
- **Health check:** Route 53 asks the server "are you OK?" over HTTP. No answer means Unhealthy.
- **Failover routing:** the Primary record is used while it's healthy. If not, Route 53 answers with the Secondary.
- **TTL:** how long other DNS servers may remember an answer. A TTL of 60 makes it faster but not instant.
- **S3 as backup:** a static page costs almost nothing and needs no second server.

My one-sentence rule: **Route 53 decides, the health check monitors, EC2 serves the primary, S3 serves the backup.**

## Challenge
Not recorded yet. I'll add what went wrong and how I fixed it after I confirm the full run.

## Validation checklist
- [x] S3 backup page created (`index.html`)
- [ ] S3 backup page loads from the website endpoint
- [ ] EC2 primary page loads directly
- [ ] Public hosted zone exists
- [ ] Health check is Healthy
- [ ] Primary and Secondary records exist
- [ ] Health check turns Unhealthy after stopping EC2
- [ ] The domain serves the S3 page during the outage
- [ ] Primary recovers after starting EC2
- [ ] Resources cleaned up

## Notes
- The backup bucket is public so visitors can read the page. Only the one page lives there.
- Route 53 charges for hosted zones and health checks, and EC2 charges while running. I clean up after testing and check Billing. I didn't repeat the "first 50 health checks are free" claim from my original notes because I haven't confirmed it, so I'll read the current Route 53 pricing page.
- From what I've read, an alias record pointing at an S3 website endpoint may need the bucket name to match the record name. I'll check this when I build the records.

Documentation was written with AI assistance (Claude) for structure and clarity. I do the labs in the AWS Console myself and check what is written here against what I did.
