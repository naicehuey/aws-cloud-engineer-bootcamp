# Route 53 Automated Failover — Study Notes

## 1. Core Architecture

```text
User / Browser
     ↓
Route 53 Public Hosted Zone
     ↓
Failover Routing Policy
     ├── Primary → EC2
     └── Secondary → S3
```

Route 53 is the DNS decision layer.

## 2. Service Roles

| Component | Job |
|---|---|
| Route 53 Hosted Zone | Holds DNS records for the domain |
| Route 53 Health Check | Monitors the primary EC2 endpoint |
| Route 53 Failover Record | Defines Primary/Secondary behavior |
| EC2 | Primary application server |
| S3 Website | Backup/maintenance website |

## 3. Normal Traffic Flow

```text
Browser
  ↓
Route 53
  ↓
Health Check = Healthy
  ↓
Primary record
  ↓
EC2 Web Server
```

Primary response:

```text
[PRIMARY ONLINE] Welcome to Huey's Production Application Server
```

## 4. Failure Traffic Flow

```text
Browser
  ↓
Route 53
  ↓
Health Check = Unhealthy
  ↓
Secondary record
  ↓
S3 Website
```

Backup response:

```text
[FAILOVER SUCCESS] Backup Endpoint Active - System Under Maintenance
```

## 5. Failover Record Structure

### Primary

```text
Name: same DNS name
Type: A
Value: EC2 public IPv4
TTL: 60
Routing policy: Failover
Failover type: Primary
Health check: Primary-EC2-HealthCheck
Record ID: Primary-EC2-Record
```

### Secondary

```text
Name: same DNS name
Type: A
Alias: S3 website endpoint where supported
Routing policy: Failover
Failover type: Secondary
Record ID: Secondary-S3-Record
```

## 6. Health Check Mental Model

```text
Route 53 Health Check
        |
        v
HTTP request to EC2:80 /
        |
        +---- responds → Healthy
        |
        +---- unavailable → Unhealthy
```

The health check does not repair EC2. It supplies health information to the routing configuration.

## 7. EC2 User Data

```bash
#!/bin/bash

dnf update -y
dnf install -y httpd

systemctl start httpd
systemctl enable httpd

echo "[PRIMARY ONLINE] Welcome to Huey's Production Application Server" > /var/www/html/index.html
```

### Command meanings

- `#!/bin/bash` — executes the script with Bash.
- `dnf update -y` — updates packages.
- `dnf install -y httpd` — installs Apache HTTP Server.
- `systemctl start httpd` — starts Apache immediately.
- `systemctl enable httpd` — enables Apache at boot.
- `echo ... > /var/www/html/index.html` — creates the page Apache serves.

## 8. S3 Backup Page

The object is:

```text
index.html
```

Example:

```html
<h1>[FAILOVER SUCCESS] Backup Endpoint Active - System Under Maintenance</h1>
```

## 9. Security

For the lab:

```text
HTTP TCP/80 → 0.0.0.0/0
```

If SSH is needed:

```text
SSH TCP/22 → YOUR_PUBLIC_IP/32
```

Avoid opening SSH to the whole internet unless there is a deliberate temporary lab reason.

## 10. DNS Concepts

### Hosted Zone

A Route 53 hosted zone contains DNS records for a domain.

### A Record

An A record maps a DNS name to an IPv4 address.

### TTL

TTL controls how long recursive DNS resolvers may cache a response. The supplied project uses `60` seconds for testing. A 60-second TTL does not guarantee instant failover.

## 11. Failover Mental Model

```text
Primary available?
      |
      +-- YES → Primary
      |
      +-- NO → Secondary
```

This differs conceptually from weighted, latency, geolocation, and simple routing policies.

## 12. What Must Be True

### S3

- [ ] Bucket exists.
- [ ] Static website hosting enabled.
- [ ] `index.html` uploaded.
- [ ] Backup page loads.
- [ ] Website endpoint known.

### EC2

- [ ] Instance running.
- [ ] Public IPv4 available.
- [ ] Apache installed.
- [ ] Apache running.
- [ ] Port 80 allowed.
- [ ] Primary page loads.

### Route 53

- [ ] Public hosted zone exists.
- [ ] Domain is delegated correctly if externally registered.
- [ ] Health check exists.
- [ ] Health check is Healthy.
- [ ] Primary failover record exists.
- [ ] Secondary failover record exists.
- [ ] Both records use the same DNS name.
- [ ] Primary has the health check attached.

## 13. Failure Test

### Before

```text
EC2 = Running
Health Check = Healthy
DNS = Primary
Website = EC2
```

### Trigger

```text
Stop EC2
```

### Expected sequence

```text
EC2 stops
    ↓
HTTP endpoint stops responding
    ↓
Health check detects failure
    ↓
Health Check = Unhealthy
    ↓
Route 53 failover logic selects secondary
    ↓
S3 backup website serves content
```

### Recovery

```text
Start EC2
    ↓
Apache becomes available
    ↓
Health Check = Healthy
    ↓
Primary becomes eligible again
```

## 14. Screenshot Checklist

| # | Screenshot | Evidence |
|---|---|---|
| 1 | `01-s3-backup-endpoint.png` | S3 backup page works |
| 2 | `02-primary-ec2-active.png` | EC2 primary page works |
| 3 | `03-route53-healthcheck-healthy.png` | Health check is Healthy |
| 4 | `04-route53-failover-records.png` | Primary + Secondary records exist |
| 5 | `05-failover-traffic-verified.png` | Backup page served after failure |

## 15. Troubleshooting Decision Tree

```text
Primary page does not load
        |
        +-- EC2 running?
        |       |
        |       +-- NO → Start instance
        |
        +-- Apache running?
        |       |
        |       +-- NO → Start httpd
        |
        +-- Port 80 allowed?
        |       |
        |       +-- NO → Fix security group
        |
        +-- Public IP correct?
                |
                +-- NO → Update configuration
```

For Route 53:

```text
Failover not occurring
        |
        +-- Health check Healthy?
        |       |
        |       +-- YES → Investigate DNS/record configuration
        |
        +-- NO → Check primary/secondary records
                    |
                    +-- Same DNS name?
                    +-- Primary has health check?
                    +-- Failover policy?
                    +-- Correct S3 target?
```

## 16. Interview Questions

### What is Route 53 doing?

It provides DNS resolution and applies the configured failover routing policy.

### What determines primary health?

The Route 53 health check monitors the configured EC2 HTTP endpoint.

### What happens when the primary fails?

When Route 53 considers the primary unhealthy, the failover configuration can return the secondary destination.

### Why use S3 as the secondary?

It can serve a simple static maintenance/backup page without requiring a second running EC2 instance.

### Does Route 53 restart EC2?

No. Route 53 performs DNS routing; it does not repair or restart the EC2 application.

### Is failover instant?

Not necessarily. Health-check detection and DNS caching affect when clients observe the change.

## 17. Cost-Safety Checklist

Before testing:

```text
[ ] One small EC2 instance
[ ] No unnecessary additional instances
[ ] Tiny S3 test site
[ ] Temporary Route 53 resources
```

After testing:

```text
[ ] Terminate EC2
[ ] Delete health check
[ ] Empty S3 bucket
[ ] Delete S3 bucket
[ ] Delete hosted zone if no longer needed
```

## 18. Memory Rule

> **Route 53 decides. Health Check monitors. EC2 serves primary. S3 serves backup.**

## 19. Architecture Chain

```text
Client
 ↓
DNS
 ↓
Route 53
 ↓
Failover Policy
 ├── Healthy → EC2
 └── Unhealthy → S3
```

Remember the relationship:

```text
Health Check → Failover Decision → Endpoint
```

## 20. Project Status

These notes are based on the supplied project specification. They intentionally do not invent actual resource IDs, domain names, or observed test results. Add those after recreating the lab.
