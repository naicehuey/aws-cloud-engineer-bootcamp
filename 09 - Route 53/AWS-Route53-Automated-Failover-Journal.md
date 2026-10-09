# Route 53 Automated Failover — Project Journal

## Project

**Project:** Route 53 Automated Failover Architecture  
**Primary:** Amazon EC2 web server  
**Secondary:** Amazon S3 static website  
**Traffic control:** Amazon Route 53 Failover routing  
**Monitoring:** Route 53 Health Check

## 1. Objective

The objective is to build a DNS-level automated failover architecture where Route 53 normally directs traffic to an EC2 application and can direct traffic to an S3 backup endpoint when the primary is considered unhealthy.

## 2. Architecture

```text
                       [ Web Client / Browser ]
                                  |
                                  v
                        [ Amazon Route 53 ]
                   (Public Hosted Zone & DNS)
                                  |
                   +--------------+--------------+
                   |                             |
         (Primary: Healthy)           (Secondary: Failover)
                   |                             |
                   v                             v
         [ EC2 Web Server ]           [ S3 Static Website ]
         (Primary Application)         (Maintenance / Backup)
```

## 3. Component Roles

### Route 53
DNS and failover decision layer.

### Health Check
Monitors the primary EC2 HTTP endpoint and provides health information for the failover configuration.

### EC2
Primary application server running Apache.

Expected response:

```text
[PRIMARY ONLINE] Welcome to Huey's Production Application Server
```

### S3
Secondary static maintenance/backup endpoint.

Expected response:

```text
[FAILOVER SUCCESS] Backup Endpoint Active - System Under Maintenance
```

## 4. Build Record

### Phase 1 — Secondary endpoint

Create and verify the S3 website first so a backup destination exists before DNS failover is configured.

Evidence: `01-s3-backup-endpoint.png`

### Phase 2 — Primary endpoint

Launch `Primary-Web-Server` using Amazon Linux 2023 and install Apache through User Data.

Evidence: `02-primary-ec2-active.png`

### Phase 3 — DNS layer

Create the Route 53 public hosted zone and delegate the domain if it is registered elsewhere.

### Phase 4 — Health monitoring

Create `Primary-EC2-HealthCheck` against the EC2 public IPv4 address on HTTP port 80 and verify Healthy status.

Evidence: `03-route53-healthcheck-healthy.png`

### Phase 5 — Failover routing

Create matching Primary and Secondary records using Route 53 Failover routing.

Evidence: `04-route53-failover-records.png`

### Phase 6 — Failure simulation

Stop the EC2 instance and observe the health check transition to Unhealthy. Then verify that the configured DNS name eventually serves the S3 backup page.

Evidence: `05-failover-traffic-verified.png`

## 5. What This Project Demonstrates

- DNS-based availability design.
- Route 53 health checks.
- Failover routing.
- EC2 as a primary application endpoint.
- S3 as a simple static backup endpoint.
- Failure simulation and recovery.

## 6. Verification Log

| Test | Expected Result | Actual Result |
|---|---|---|
| S3 direct test | Backup page loads | Record after recreation |
| EC2 direct test | Primary page loads | Record after recreation |
| Health check | Healthy | Record after recreation |
| Failover records | Primary + Secondary visible | Record after recreation |
| EC2 outage | Primary unavailable | Record after recreation |
| Health check after outage | Unhealthy | Record after recreation |
| DNS failover | S3 page loads | Record after recreation |
| EC2 recovery | Primary available again | Record after recreation |
| Cleanup | Temporary resources removed | Record after recreation |

## 7. Lessons

### Lesson 1 — DNS can participate in availability design

Route 53 is used as the DNS control layer and can apply a failover routing policy based on endpoint health information.

### Lesson 2 — Health checks and routing work together

The health check provides endpoint health information; the failover routing policy uses that information when selecting the DNS response.

### Lesson 3 — Primary and secondary endpoints have different responsibilities

EC2 is the normal application endpoint. S3 is the backup/maintenance endpoint.

### Lesson 4 — Failure testing is essential

The architecture should be tested by deliberately making the primary unavailable rather than only confirming that the records exist.

### Lesson 5 — DNS failover is not necessarily instantaneous

Health-check detection and DNS caching can affect when clients observe the new endpoint.

## 8. Cost Control

Treat the lab as temporary. Keep the architecture small, terminate the EC2 instance after testing, delete the health check, empty/delete the S3 bucket, and delete the hosted zone if it is no longer required.

Current AWS pricing should be verified before rebuilding because the supplied cost assumptions can change.

## 9. Troubleshooting Notes

### Health check remains unhealthy

Check:

- EC2 is running.
- Apache is running.
- Port 80 is reachable.
- Security group permits HTTP.
- Public IPv4 is correct.
- Health check points to the current IP.
- `/` returns a successful web response.

### DNS does not immediately show the backup

Check:

- Health check state.
- Primary/secondary record configuration.
- DNS name.
- Routing policy.
- TTL and DNS caching.

### S3 page does not load

Check:

- Static website hosting.
- `index.html` exists.
- Bucket policy uses the correct bucket name.
- Correct website endpoint and region.

## 10. Final Reflection

The architecture connects:

```text
EC2
 ↓
HTTP application
 ↓
Route 53 Health Check
 ↓
Route 53 Failover Routing
 ↓
S3 Backup Endpoint
```

The core mental model is:

> **Route 53 makes the DNS decision, the health check supplies endpoint health information, EC2 provides the primary application, and S3 provides the backup endpoint.**

## Project Status

This journal is based on the supplied project specification. Actual resource IDs, domain names, timestamps, screenshots, and observed failover results should be recorded after the lab is recreated.
