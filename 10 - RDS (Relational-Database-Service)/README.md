# Amazon RDS Multi-AZ PostgreSQL Architecture

## Overview

This project demonstrates a managed PostgreSQL database architecture using Amazon RDS, Amazon EC2, security groups, Multi-AZ database deployment, PostgreSQL connectivity, SQL operations, and a manual RDS snapshot.

```text
                          [ Internet / User ]
                                   |
                                   v
                       [ EC2 Web/App Server ]
                        (Public Subnet - SG)
                                   |
                                   | TCP 5432
                                   v
                       [ Security Group Rule ]
                  (Allows inbound only from EC2 SG)
                                   |
                   +---------------+---------------+
                   |                               |
        [ Primary RDS Instance ]        [ Standby RDS Instance ]
         (PostgreSQL - AZ 1)             (Multi-AZ Sync - AZ 2)
```

## Portfolio Deliverables

| Screenshot | Evidence |
|---|---|
| `01-rds-security-group-rules.png` | RDS security group allows PostgreSQL 5432 only from EC2 security group |
| `02-rds-database-available.png` | RDS PostgreSQL database is Available |
| `03-ec2-rds-connection.png` | EC2 successfully connects to PostgreSQL with `psql` |
| `04-rds-query-execution.png` | SQL table creation, inserts, and SELECT output |
| `05-rds-manual-snapshot.png` | Completed manual RDS snapshot |

# Cost Safety Strategy

This is a temporary portfolio lab.

- Use the smallest suitable EC2 instance.
- Use the smallest suitable RDS instance.
- Do not create unnecessary EC2 instances.
- Do not leave the database running after the lab.
- Delete the manual snapshot when it is no longer required.
- Terminate the EC2 instance after testing.
- Delete the RDS database after the portfolio evidence is captured.

**Important:** AWS Free Tier eligibility and pricing can change. Verify current AWS pricing and your account eligibility before creating a Multi-AZ RDS database.

# Step 1 — Create the Security Groups

The database should not be open to the public internet. The intended relationship is:

```text
EC2 SG → TCP 5432 → RDS SG → PostgreSQL
```

## EC2 security group

Open **AWS Console → VPC → Security Groups → Create security group**.

Use:

```text
Security group name: ec2-app-sg
Description: Security group for public EC2 application server
VPC: Default VPC
```

Inbound:

| Type | Port | Source |
|---|---:|---|
| SSH | 22 | My IP |

Create it.

## RDS security group

Create another group:

```text
Security group name: rds-postgres-sg
Description: Security group for private RDS PostgreSQL database
VPC: Default VPC
```

Inbound:

```text
Type: PostgreSQL
Port: 5432
Source: Custom → ec2-app-sg
```

Select the actual security-group ID for `ec2-app-sg`.

Do **not** use `0.0.0.0/0` for database access.

### Screenshot

**`01-rds-security-group-rules.png`** — Capture the inbound rules of `rds-postgres-sg` showing PostgreSQL 5432 restricted to the EC2 security group.

# Step 2 — Provision the Amazon RDS PostgreSQL Database

Open **AWS Console → Amazon RDS → Databases → Create database**.

Configure:

```text
Creation method: Standard create
Engine: PostgreSQL
Template: Free tier (or Dev/Test when required for the lab)
DB instance identifier: huey-postgres-db
Master username: postgres
```

Use a strong password of your own rather than publishing a real password in GitHub.

## Instance configuration

```text
DB instance class: db.t3.micro or db.t4g.micro
```

## Storage

```text
Storage type: gp3
Allocated storage: 20 GiB
```

## Connectivity

```text
Compute resource: Don't connect to an EC2 compute resource
VPC: Default VPC
Public access: No
```

Remove the default security group if selected and choose:

```text
rds-postgres-sg
```

Availability Zone:

```text
No preference
```

## Additional configuration

```text
Initial database name: appdb
```

Create the database and wait for:

```text
Status: Available
```

Record the generated endpoint and port 5432.

### Screenshot

**`02-rds-database-available.png`** — Capture the RDS dashboard showing `huey-postgres-db`, status **Available**, endpoint, and port 5432.

# Step 3 — Launch the EC2 Application Server

Open **AWS Console → EC2 → Launch instance**.

Use:

```text
Name: App-Jump-Server
AMI: Amazon Linux 2023
Instance type: t3.micro
```

Network settings:

```text
Security group: ec2-app-sg
Auto-assign public IP: Enable
```

Launch the instance.

The EC2 instance provides the environment from which the PostgreSQL client connects to the private RDS database.

# Step 4 — Connect From EC2 to RDS

Connect to `App-Jump-Server` using EC2 Instance Connect or SSH.

Install the PostgreSQL client:

```bash
sudo dnf update -y
sudo dnf install -y postgresql15
```

Verify:

```bash
psql --version
```

Find the RDS endpoint under **RDS → Databases → huey-postgres-db → Connectivity & security**.

Connect:

```bash
psql -h YOUR-RDS-ENDPOINT-HERE -U postgres -d appdb
```

Enter the database password when prompted.

Successful authentication should produce:

```text
appdb=>
```

### Screenshot

**`03-ec2-rds-connection.png`** — Capture the EC2 terminal showing the PostgreSQL `appdb=>` prompt.

# Step 5 — Execute Database Operations

Create the application table:

```sql
CREATE TABLE system_logs (
    log_id SERIAL PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Insert the sample records:

```sql
INSERT INTO system_logs (service_name, status) 
VALUES 
    ('AuthService', 'HEALTHY'),
    ('PaymentGateway', 'HEALTHY'),
    ('NotificationEngine', 'DEGRADED');
```

Query the records:

```sql
SELECT log_id, service_name, status, created_at
FROM system_logs;
```

Expected logical result:

```text
AuthService          HEALTHY
PaymentGateway      HEALTHY
NotificationEngine  DEGRADED
```

The timestamps will be generated by your database.

### Screenshot

**`04-rds-query-execution.png`** — Capture the terminal showing table creation, insertion, and returned SELECT data.

Exit PostgreSQL with:

```text
\q
```

# Step 6 — Understand the Multi-AZ Architecture

The intended design is:

```text
                 RDS PostgreSQL
                       |
          +------------+------------+
          |                         |
          v                         v
       Primary                   Standby
        AZ 1                      AZ 2
          \                       /
           \__ Synchronous ______/
               replication
```

The application uses the RDS endpoint rather than manually selecting a primary or standby instance.

The key mental model is:

```text
Application → RDS endpoint → Current primary
```

RDS manages the infrastructure-level Multi-AZ failover process.

# Step 7 — Create a Manual Database Snapshot

Open **RDS → Databases → huey-postgres-db**.

Choose **Actions → Take snapshot**.

Use:

```text
huey-postgres-db-manual-snapshot
```

Go to **RDS → Snapshots** and wait until:

```text
Status: Available
```

### Screenshot

**`05-rds-manual-snapshot.png`** — Capture the snapshot showing `huey-postgres-db-manual-snapshot` with status **Available**.

# Verification Checklist

- [ ] `ec2-app-sg` exists.
- [ ] `rds-postgres-sg` exists.
- [ ] RDS allows TCP 5432 only from `ec2-app-sg`.
- [ ] RDS Public access is No.
- [ ] RDS database is Available.
- [ ] RDS endpoint and port 5432 are recorded.
- [ ] `App-Jump-Server` is running.
- [ ] PostgreSQL client is installed.
- [ ] EC2 can connect to RDS.
- [ ] `system_logs` table exists.
- [ ] Three records are inserted.
- [ ] SELECT returns the records.
- [ ] Manual snapshot is Available.

# Troubleshooting

## `psql` cannot connect

Check:

1. EC2 and RDS are in the same VPC.
2. RDS security group allows PostgreSQL 5432 from `ec2-app-sg`.
3. EC2 uses `ec2-app-sg`.
4. RDS status is Available.
5. The endpoint is correct.
6. PostgreSQL client is installed.

## Connection times out

Inspect the path:

```text
EC2 → TCP 5432 → RDS security group → RDS
```

Do not make the database public simply to bypass a configuration problem.

## Authentication fails

Check the username, password, endpoint, database name, and port.

Connection format:

```bash
psql -h ENDPOINT -U USERNAME -d DATABASE
```

# Cleanup

After evidence is captured:

1. Exit `psql`.
2. Terminate `App-Jump-Server`.
3. Delete `huey-postgres-db`.
4. Delete `huey-postgres-db-manual-snapshot` when no longer required.
5. Delete `ec2-app-sg` when unused.
6. Delete `rds-postgres-sg` when unused.

# GitHub Evidence

```text
screenshots/
├── 01-rds-security-group-rules.png
├── 02-rds-database-available.png
├── 03-ec2-rds-connection.png
├── 04-rds-query-execution.png
└── 05-rds-manual-snapshot.png
```

# Architecture Memory Rule

> **EC2 is the application client, the EC2 security group identifies who may access the database, the RDS security group controls PostgreSQL access on port 5432, RDS manages PostgreSQL, Multi-AZ provides a standby, and snapshots provide a recoverable backup.**

# Project Status

This README documents the supplied Amazon RDS Multi-AZ PostgreSQL architecture and recreation procedure. Add actual resource IDs, endpoint, query output, snapshot ID, and screenshots after the lab is recreated.
