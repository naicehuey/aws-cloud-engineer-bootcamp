# Project 10 — Learning Notes

## Core flow
```text
EC2 (ec2-app-sg) --TCP 5432--> RDS (rds-postgres-sg: allows only ec2-app-sg) --> PostgreSQL
```

## Components
| Component | Role |
|---|---|
| EC2 | App / jump server where I run `psql` |
| `ec2-app-sg` | Controls access to EC2 (SSH from my IP) |
| `rds-postgres-sg` | Controls access to the database (5432 from EC2 SG) |
| RDS PostgreSQL | Managed database |
| Multi-AZ | Standby in another zone for availability |
| Snapshot | Backup / recovery point |

## Security rule
Wrong: PostgreSQL, 5432, source `0.0.0.0/0`.
Right: PostgreSQL, 5432, source `ec2-app-sg`.

## psql
```bash
psql -h <endpoint> -U postgres -d appdb
```
- `-h` host, `-U` user, `-d` database. Exit with `\q`.

## SQL used (`project/system_logs.sql`)
```sql
CREATE TABLE system_logs (
    log_id SERIAL PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO system_logs (service_name, status) VALUES
  ('AuthService','HEALTHY'), ('PaymentGateway','HEALTHY'), ('NotificationEngine','DEGRADED');
SELECT log_id, service_name, status, created_at FROM system_logs;
```
| Column | Purpose |
|---|---|
| `log_id` | unique ID that counts up by itself |
| `service_name` | which service |
| `status` | HEALTHY or DEGRADED |
| `created_at` | set automatically |

## Multi-AZ vs snapshot
- Multi-AZ: availability and failover. The app keeps using the same endpoint.
- Snapshot: backup and recovery.
- Memory: Multi-AZ keeps the service up. A snapshot lets me get data back.
- To check Multi-AZ is on: open the database, Configuration tab. (It has to be chosen when creating the database.)

## Why EC2 is public but RDS is not
EC2 has a public IP so I can administer it in the lab. RDS stays private. Public EC2 doesn't mean public database.

## Troubleshooting
```text
Timeout / could not connect  -> network
  RDS Available? Right endpoint? EC2 uses ec2-app-sg? rds-postgres-sg allows 5432 from it? Same VPC?
Password failed / database or role does not exist -> login problem
  Check user, password, database name (appdb).
```
Don't make the database public to bypass a problem.

## Cost awareness
Terminate EC2, delete the database, delete the snapshot when not needed, delete unused security groups. Multi-AZ costs more.

## Self-test
1. Why is RDS not public?
2. What port does PostgreSQL use?
3. How does RDS know which app may connect?
4. Why use a security group as the source?
5. What does Multi-AZ give me?
6. Does the app connect to the standby directly?
7. Is Multi-AZ a backup?
8. Why use RDS and not PostgreSQL on EC2?

### Answers
1. To avoid exposing the database; the app reaches it privately.
2. TCP 5432.
3. The RDS security group allows 5432 only from the EC2 security group.
4. It limits access to the intended app, not the whole internet.
5. A standby in another zone for availability and failover.
6. No. It uses the RDS endpoint.
7. No. Snapshots are the backup.
8. RDS is managed, so I do less database administration.

## One-sentence memory rule
> **EC2 runs the app, RDS runs PostgreSQL, port 5432 carries the traffic, the RDS security group trusts the EC2 security group, Multi-AZ gives a standby, and snapshots give recovery.**
