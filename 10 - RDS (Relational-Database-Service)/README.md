# Project 10 — RDS PostgreSQL with Multi-AZ

## Overview
My first managed database on AWS. I put a PostgreSQL database on Amazon RDS, kept it private inside the VPC, and connected to it from an EC2 server. A security group rule makes sure only that server can reach the database on port 5432. I then created a table, inserted rows, queried them, and took a manual snapshot as a backup. I'm still learning RDS, so this README records the plan and what I have evidence for so far.

> **Status:** the documentation and SQL are ready. The sections marked "to confirm" need my screenshots and results, and I still need to check whether Multi-AZ was really turned on (see Notes).

## Stack
Amazon RDS (PostgreSQL) · Amazon EC2 (Amazon Linux 2023) · VPC security groups · `psql` · AWS Management Console

## What I practiced
- Keeping a database private (Public access: No)
- Security group rules that use another security group as the source
- Creating an RDS PostgreSQL instance
- Connecting from EC2 with `psql`
- Creating a table, inserting rows and running a query
- Taking a manual snapshot
- Understanding Multi-AZ (availability) compared with snapshots (backup)

## Configuration (plan)
| Item | Value |
|---|---|
| EC2 security group | `ec2-app-sg`, SSH 22 from My IP |
| RDS security group | `rds-postgres-sg`, PostgreSQL 5432 from `ec2-app-sg` only |
| Database identifier | `huey-postgres-db` |
| Engine | PostgreSQL |
| Instance class | `db.t3.micro` or `db.t4g.micro` |
| Storage | gp3, 20 GiB |
| Public access | No |
| Initial database | `appdb` |
| Master user | `postgres` (password kept private) |
| EC2 server | `App-Jump-Server`, Amazon Linux 2023, `t3.micro` |
| Snapshot | `huey-postgres-db-manual-snapshot` |
| VPC | Default VPC |

## Project structure
```text
10-rds/
├── project/
│   └── system_logs.sql        # table, rows and query
├── documentation/
│   ├── RDS-Journal.md
│   └── RDS-Notes.md
├── architecture/
│   └── RDS-Architecture-Diagram.md
├── screenshots/
│   ├── 01-rds-security-group-rules.png
│   ├── 02-rds-database-available.png
│   ├── 03-ec2-rds-connection.png
│   ├── 04-rds-query-execution.png
│   └── 05-rds-manual-snapshot.png
└── README.md
```

## Architecture
```text
User / admin
     |  SSH (my IP only)
     v
+------------------+   TCP 5432   +----------------------+
| EC2 App server   | -----------> | RDS PostgreSQL       |
| ec2-app-sg       |  allowed     | rds-postgres-sg      |
| (public subnet)  |  only from   | Public access: No    |
+------------------+  ec2-app-sg  +----------+-----------+
                                             |
                          +------------------+------------------+
                          |                                     |
                    Primary (AZ 1)  <-- sync replication -->  Standby (AZ 2)
                                             |
                                       Manual snapshot
```

## Screenshots
Add these after hiding account IDs, the RDS endpoint and public IPs:

1. `01-rds-security-group-rules.png` — RDS rule: 5432 from the EC2 security group
2. `02-rds-database-available.png` — database status Available, port 5432
3. `03-ec2-rds-connection.png` — the `appdb=>` prompt
4. `04-rds-query-execution.png` — CREATE TABLE, INSERT, SELECT and the three rows
5. `05-rds-manual-snapshot.png` — snapshot status Available

## What I did (plan)
1. Create `ec2-app-sg` and `rds-postgres-sg`, with 5432 allowed only from `ec2-app-sg`. (to confirm)
2. Create the RDS PostgreSQL database `huey-postgres-db` with Public access: No. (to confirm)
3. Launch `App-Jump-Server` in `ec2-app-sg`. (to confirm)
4. Install the client and connect: `sudo dnf install -y postgresql15` then `psql -h <endpoint> -U postgres -d appdb`. (to confirm)
5. Run `project/system_logs.sql`. (to confirm)
6. Take the manual snapshot and wait for Available. (to confirm)
7. Delete the database, snapshot, EC2 and security groups. (to confirm)

## Key ideas (in my own words)
- **RDS** is PostgreSQL that AWS manages for me, so I don't install or patch it on a server.
- **Private database:** only my EC2 server can reach it, not the internet.
- **Security group as a source:** instead of an IP range, the rule says "allow whoever is in `ec2-app-sg`".
- **Port 5432:** the PostgreSQL port.
- **Multi-AZ:** a standby copy in another zone, for availability. It is not a backup.
- **Snapshot:** a backup I can restore from. It is not for availability.

My one-sentence rule: **EC2 runs the app, RDS runs PostgreSQL, port 5432 carries the traffic, the RDS security group trusts the EC2 security group, Multi-AZ gives a standby, and snapshots give recovery.**

## Challenge
Not recorded yet. I'll add any problems (timeouts, wrong endpoint, password errors) and how I fixed them.

## Validation checklist
- [ ] Both security groups exist
- [ ] RDS allows 5432 only from `ec2-app-sg`
- [ ] Public access is No
- [ ] Database status is Available
- [ ] EC2 connects with `psql` (`appdb=>`)
- [ ] `system_logs` created, 3 rows inserted, SELECT returns them
- [ ] Multi-AZ confirmed as enabled (Configuration tab shows Multi-AZ: Yes)
- [ ] Manual snapshot is Available
- [ ] Resources deleted

## Notes
- **Multi-AZ check:** my original steps never actually switch Multi-AZ on. They only say "Availability Zone: No preference". As far as I know, the Free tier template doesn't offer Multi-AZ, and it has to be chosen under Availability and durability when creating the database. I'll check the Configuration tab of my database before I write "Multi-AZ" in my CV or on LinkedIn. If it was single-AZ, I'll document it that way, or redo it with Multi-AZ for a short time to practise.
- Multi-AZ roughly doubles the database cost, and RDS charges by the hour while it exists. I delete the database, the snapshot and the EC2 server when I'm done and check Billing. Snapshots also cost storage while they exist.
- I never put the database password or the real endpoint in GitHub.

Documentation was written with AI assistance (Claude) for structure and clarity. I do the labs in the AWS Console myself and check what is written here against what I did.
