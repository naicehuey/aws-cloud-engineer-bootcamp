# Project 09 — Learning Notes

## Core flow
```text
Browser -> Route 53 -> health check Healthy?   -> yes -> EC2 (primary)
                                               -> no  -> S3 website (secondary)
```

## Components
| Component | Job |
|---|---|
| Hosted zone | Holds the DNS records for my domain |
| Health check | Sends HTTP requests to EC2 and reports Healthy or Unhealthy |
| Failover records | One Primary and one Secondary with the same name |
| EC2 | Primary web server |
| S3 website | Backup page |

## Records
**Primary:** type A, value = EC2 public IPv4, TTL 60, Failover = Primary, health check attached.
**Secondary:** type A, alias to the S3 website endpoint, Failover = Secondary.

## EC2 User Data
```bash
#!/bin/bash
dnf update -y
dnf install -y httpd
systemctl start httpd
systemctl enable httpd
echo "[PRIMARY ONLINE] Welcome to Huey's Production Application Server" > /var/www/html/index.html
```
- `dnf install -y httpd`: installs Apache
- `systemctl start httpd`: starts it now
- `systemctl enable httpd`: starts it at every boot
- `echo ... > index.html`: creates the page Apache serves

## S3 backup page
Needs: static website hosting on, `index.html` uploaded, a bucket policy allowing public `s3:GetObject`, and Block Public Access off for the lab.

## Concepts
- **A record:** name to IPv4 address.
- **TTL:** how long resolvers may cache the answer. 60 seconds doesn't mean instant.
- **Failover vs other policies:** failover is "primary if healthy, otherwise secondary". Weighted, latency and geolocation split traffic instead.
- **Route 53 doesn't fix EC2.** It only changes where DNS points.

## Failure test
```text
Before: EC2 running, health check Healthy, domain shows EC2
Stop EC2 -> health check turns Unhealthy -> domain shows the S3 page
Start EC2 -> Apache up -> Healthy -> primary is used again
```

## Troubleshooting
```text
Health check Unhealthy while EC2 is running?
  - Apache running?   - port 80 allowed in the security group?
  - IP in the check is the current public IP?   - "/" returns a page?

Backup not showing?
  - Health check really Unhealthy?   - Same name on both records?
  - Primary has the health check attached?   - TTL / caching?
  - S3 website hosting on, index.html present, policy has the right bucket name?
```

## Cost awareness
Terminate EC2, delete the health check, empty and delete the bucket, delete the hosted zone if not needed. Deleting a hosted zone doesn't cancel a domain registration.

## Self-test
1. What does Route 53 do in this project?
2. What does the health check do?
3. What happens when it reports Unhealthy?
4. Does Route 53 restart EC2?
5. Why use S3 as the secondary?
6. Is failover instant?

### Answers
1. DNS answers and the failover routing decision.
2. Sends HTTP requests to EC2 and reports its health.
3. Route 53 answers with the Secondary record (the S3 page).
4. No. It only changes the DNS answer.
5. It serves a static page without a second server and costs very little.
6. No. Health check detection and DNS caching add delay.

## One-sentence memory rule
> **Route 53 decides, the health check monitors, EC2 serves the primary, S3 serves the backup.**
