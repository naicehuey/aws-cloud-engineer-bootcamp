# Project 10 — Architecture

```text
              Admin (SSH, my IP only)
                      |
                      v
        +---------------------------+
        | EC2: App-Jump-Server      |
        | SG: ec2-app-sg            |
        | (public subnet)           |
        +-------------+-------------+
                      |
                      |  TCP 5432 (psql)
                      v
        +---------------------------+
        | SG: rds-postgres-sg       |
        | allows 5432 from          |
        | ec2-app-sg only           |
        +-------------+-------------+
                      |
                      v
        +---------------------------+
        | RDS PostgreSQL            |
        | huey-postgres-db          |
        | Public access: No         |
        +------+------------+-------+
               |            |
        Primary (AZ 1)   Standby (AZ 2)
               |         (Multi-AZ, to confirm)
               v
        +---------------------------+
        | Manual snapshot           |
        | (backup)                  |
        +---------------------------+
```
