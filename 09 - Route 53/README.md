# Route 53 Automated Failover Architecture

## Overview

This project demonstrates an automated DNS failover architecture using Amazon Route 53, a primary Amazon EC2 web server, and a secondary Amazon S3 static website.

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

## AWS Services

| Service | Purpose |
|---|---|
| Amazon Route 53 | DNS resolution and failover routing |
| Route 53 Health Check | Monitors the primary EC2 endpoint |
| Amazon EC2 | Hosts the primary application |
| Amazon S3 | Hosts the backup static website |

## Cost Safety Strategy

The supplied project specification assumes:

- Route 53 Hosted Zone: approximately $0.50/month, prorated according to the original notes.
- EC2: one `t3.micro`, stopped or terminated immediately after testing.
- S3: minimal storage/request usage for the small backup page.
- Route 53 Health Check: the original notes state that the first 50 basic health checks are free.

Pricing changes over time, so verify current AWS pricing before recreating the lab.

## Step 1 — Create the Secondary S3 Backup Site

1. Open **AWS Console → S3 → Create bucket**.
2. Use a unique bucket name, for example `backup-site-huey-2026`.
3. For this lab, disable **Block all public access** and acknowledge the warning.
4. Create the bucket.
5. Open **Properties → Static website hosting → Edit**.
6. Enable static website hosting and set the index document to `index.html`.
7. Under **Permissions → Bucket policy**, use:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
    }
  ]
}
```

Replace `YOUR-BUCKET-NAME` with the actual bucket name.

8. Upload an `index.html` containing:

```html
<h1>[FAILOVER SUCCESS] Backup Endpoint Active - System Under Maintenance</h1>
```

9. Copy the **Bucket website endpoint** and test it in a browser.

**Screenshot #1 — `01-s3-backup-endpoint.png`**: browser showing the S3 backup page.

## Step 2 — Create the Primary EC2 Web Server

1. Open **EC2 → Launch instance**.
2. Name: `Primary-Web-Server`.
3. AMI: **Amazon Linux 2023**.
4. Instance type: `t3.micro`.
5. Enable auto-assigned public IPv4.
6. Create a security group allowing HTTP TCP/80 from `0.0.0.0/0`. If SSH is required, restrict TCP/22 to your own public IP/32.
7. Under **Advanced details → User data**, use:

```bash
#!/bin/bash

dnf update -y
dnf install -y httpd

systemctl start httpd
systemctl enable httpd

echo "[PRIMARY ONLINE] Welcome to Huey's Production Application Server" > /var/www/html/index.html
```

8. Launch the instance.
9. When it is running, copy its public IPv4 address and open `http://PUBLIC-IP`.

Expected result:

```text
[PRIMARY ONLINE] Welcome to Huey's Production Application Server
```

**Screenshot #2 — `02-primary-ec2-active.png`**: browser showing the primary page.

## Step 3 — Create the Route 53 Public Hosted Zone

1. Open **Route 53 → Hosted zones**.
2. Click **Create hosted zone**.
3. Enter a domain you control.
4. Select **Public hosted zone**.
5. Create the hosted zone.

If the domain is registered with an external registrar, update the registrar's name-server records with the four Route 53 NS values shown in the hosted zone.

## Step 4 — Create the Route 53 Health Check

1. Open **Route 53 → Health checks → Create health check**.
2. Name: `Primary-EC2-HealthCheck`.
3. Monitoring type: **Endpoint**.
4. Specify endpoint by **IP address**.
5. Protocol: **HTTP**.
6. IP address: the EC2 public IPv4 address.
7. Port: `80`.
8. Path: `/`.
9. Continue and create the health check.
10. Wait for it to report **Healthy**.

**Screenshot #3 — `03-route53-healthcheck-healthy.png`**: Route 53 Health Checks showing the primary check as Healthy.

## Step 5 — Configure Route 53 Failover Records

### Primary record

Create a record with:

- Record name: blank or `app`
- Type: `A`
- Value: EC2 public IPv4
- TTL: `60`
- Routing policy: **Failover**
- Failover record type: **Primary**
- Health check: `Primary-EC2-HealthCheck`
- Record ID: `Primary-EC2-Record`

### Secondary record

Create another record with the same name:

- Type: `A`
- Alias: enabled where the console supports the required S3 website endpoint target
- Target: S3 website endpoint
- Region: the S3 bucket's region
- Routing policy: **Failover**
- Failover record type: **Secondary**
- Record ID: `Secondary-S3-Record`

**Screenshot #4 — `04-route53-failover-records.png`**: hosted zone showing both failover records.

## Step 6 — Simulate Outage and Verify Failover

1. Open **EC2 → Instances**.
2. Select `Primary-Web-Server`.
3. Choose **Instance state → Stop instance**.
4. Return to **Route 53 → Health checks**.
5. Wait for the health check to become **Unhealthy**. The supplied specification expects roughly 1–2 minutes, but actual timing can vary.
6. Open the configured domain/hostname.

Expected backup result:

```text
[FAILOVER SUCCESS] Backup Endpoint Active - System Under Maintenance
```

**Screenshot #5 — `05-failover-traffic-verified.png`**: browser showing the backup page after the primary has failed.

## Step 7 — Restore and Clean Up

Start the EC2 instance again and wait for Apache and the health check to recover.

Then remove temporary resources:

1. Terminate the EC2 instance.
2. Delete the Route 53 health check.
3. Delete the Route 53 hosted zone if it is no longer needed.
4. Empty the S3 bucket.
5. Delete the S3 bucket.

If the domain is registered separately, deleting the hosted zone does not cancel the domain registration.

## Verification Checklist

- [ ] S3 backup website loads directly.
- [ ] EC2 primary website loads directly.
- [ ] Route 53 hosted zone exists.
- [ ] Primary health check is Healthy.
- [ ] Primary and secondary failover records exist.
- [ ] Primary EC2 is stopped for the outage test.
- [ ] Health check becomes Unhealthy.
- [ ] DNS eventually serves the S3 backup endpoint.
- [ ] Primary EC2 can be restored.
- [ ] Health check returns to Healthy.
- [ ] Temporary resources are cleaned up.

## Key Concepts

> **Route 53 decides where DNS traffic should go, the health check supplies endpoint health information, EC2 serves the primary application, and S3 provides the backup endpoint.**

## Evidence

```text
screenshots/
├── 01-s3-backup-endpoint.png
├── 02-primary-ec2-active.png
├── 03-route53-healthcheck-healthy.png
├── 04-route53-failover-records.png
└── 05-failover-traffic-verified.png
```
