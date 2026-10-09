# Amazon RDS Multi-AZ PostgreSQL — Project Journal

## Project

**Project:** Amazon RDS Multi-AZ PostgreSQL Architecture  
**Primary:** Amazon RDS PostgreSQL  
**Application:** Amazon EC2  
**Network security:** VPC Security Groups  
**Availability:** RDS Multi-AZ  
**Backup:** Manual RDS Snapshot

---

# 1. Objective

The objective of this project is to build a secure managed PostgreSQL database architecture.

The application server runs on EC2 while PostgreSQL is managed by Amazon RDS.

The database is intentionally not exposed directly to the public internet.

```text
Internet / User
      |
      v
EC2 Application Server
      |
      | TCP 5432
      v
RDS Security Group
      |
      v
RDS PostgreSQL
```

The project also demonstrates Multi-AZ database availability and manual database backup using an RDS snapshot.

# 2. Architecture

```text
                          [ Internet / User ]
                                   |
                                   v
                       [ EC2 Web/App Server ]
                        (Public Subnet - SG)
                                   |
                                   | (Port 5432)
                                   v
                       [ Security Group Rule ]
                  (Allows inbound only from EC2 SG)
                                   |
                   +---------------+---------------+
                   |                               |
        [ Primary RDS Instance ]        [ Standby RDS Instance ]
         (PostgreSQL - AZ 1)             (Multi-AZ Sync - AZ 2)
```

# 3. Build Record

## Phase 1 — Security Groups

Two security groups are created.

### EC2

```text
ec2-app-sg
```

SSH:

```text
TCP 22
Source: My IP
```

### RDS

```text
rds-postgres-sg
```

PostgreSQL:

```text
TCP 5432
Source: ec2-app-sg
```

The important security relationship is:

```text
EC2 SG → RDS SG
```

Evidence:

```text
01-rds-security-group-rules.png
```

# 4. RDS Provisioning

The supplied project configuration is:

```text
Identifier: huey-postgres-db
Engine: PostgreSQL
Master username: postgres
Instance: db.t3.micro or db.t4g.micro
Storage: gp3, 20 GiB
Public access: No
Initial database: appdb
```

The database is intended to remain private inside the VPC.

Evidence:

```text
02-rds-database-available.png
```

# 5. EC2 Application Server

```text
Name: App-Jump-Server
AMI: Amazon Linux 2023
Instance: t3.micro
Security group: ec2-app-sg
```

The EC2 instance provides the environment from which the PostgreSQL client connects to RDS.

# 6. Database Connection

Install the client:

```bash
sudo dnf update -y
sudo dnf install -y postgresql15
```

Connect:

```bash
psql -h YOUR-RDS-ENDPOINT-HERE -U postgres -d appdb
```

Successful connection:

```text
appdb=>
```

Evidence:

```text
03-ec2-rds-connection.png
```

# 7. Database Operations

The project creates `system_logs`:

```sql
CREATE TABLE system_logs (
    log_id SERIAL PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Three records are inserted:

```sql
INSERT INTO system_logs (service_name, status) 
VALUES 
    ('AuthService', 'HEALTHY'),
    ('PaymentGateway', 'HEALTHY'),
    ('NotificationEngine', 'DEGRADED');
```

The query is:

```sql
SELECT log_id, service_name, status, created_at
FROM system_logs;
```

Evidence:

```text
04-rds-query-execution.png
```

# 8. Multi-AZ Understanding

The architecture is intended to use:

```text
AZ 1
Primary RDS
  |
  | synchronous Multi-AZ replication
  v
AZ 2
Standby RDS
```

The application uses the RDS endpoint rather than manually selecting the standby.

The core relationship is:

```text
Application → RDS endpoint → Current primary
```

# 9. Manual Snapshot

A manual snapshot is created:

```text
huey-postgres-db-manual-snapshot
```

The target completed state is:

```text
Status: Available
```

Evidence:

```text
05-rds-manual-snapshot.png
```

# 10. What I Learned

## Lesson 1 — Keep the database private

The project uses:

```text
Public access: No
```

The application accesses the database privately.

## Lesson 2 — Security groups can reference security groups

The RDS rule uses the EC2 security group as its source:

```text
EC2 SG → RDS SG → TCP 5432
```

## Lesson 3 — PostgreSQL uses TCP 5432

The database communication path is:

```text
EC2 → TCP 5432 → RDS
```

## Lesson 4 — RDS is managed PostgreSQL

The database infrastructure is provided and managed through Amazon RDS instead of manually installing PostgreSQL on EC2.

## Lesson 5 — Multi-AZ is about availability

The Multi-AZ design maintains a standby in another Availability Zone for managed failover.

## Lesson 6 — Snapshots provide recovery points

A manual RDS snapshot provides a backup/recovery artifact separate from the live database instance.

# 11. Verification Log

| Test | Expected Result | Actual Result |
|---|---|---|
| EC2 security group | SSH from My IP | Record after recreation |
| RDS security group | TCP 5432 from EC2 SG only | Record after recreation |
| RDS database | Available | Record after recreation |
| Public access | No | Record after recreation |
| EC2 → RDS | `psql` connection succeeds | Record after recreation |
| Table creation | `CREATE TABLE` | Record after recreation |
| Insert | 3 records inserted | Record after recreation |
| SELECT | 3 records returned | Record after recreation |
| Snapshot | Available | Record after recreation |

# 12. Evidence

```text
screenshots/
├── 01-rds-security-group-rules.png
├── 02-rds-database-available.png
├── 03-ec2-rds-connection.png
├── 04-rds-query-execution.png
└── 05-rds-manual-snapshot.png
```

# 13. Troubleshooting Notes

If EC2 cannot connect, inspect:

```text
EC2
 ↓
EC2 Security Group
 ↓
TCP 5432
 ↓
RDS Security Group
 ↓
RDS
```

Check the VPC, RDS status, endpoint, EC2 security group, RDS security group, port 5432, database name, username, and password.

# 14. Cost Control

This is a temporary portfolio project.

Intended cleanup:

```text
Terminate EC2
      ↓
Delete RDS database
      ↓
Delete manual snapshot when no longer needed
      ↓
Delete unused security groups
```

# 15. Final Reflection

This project connects:

```text
EC2
 ↓
Security Group
 ↓
TCP 5432
 ↓
RDS PostgreSQL
 ↓
Multi-AZ
 ↓
Manual Snapshot
```

The most important architectural lesson is that the database can remain private while the application communicates with it through controlled security-group access.

# 16. Project Status

**Status:** Architecture and recreation procedure documented.

Actual resource IDs, endpoint, database output, snapshot completion time, and screenshots should be added after the project is recreated.
