# Project 10 — Project Journal

**Date:** Not recorded

## Goal
Run PostgreSQL on a managed AWS database that only my application server can reach, and practise basic SQL and backups.

## Work completed
- Documentation, SQL file and diagram are written.
- The build steps (security groups, RDS, EC2, connection, SQL, snapshot) are to confirm once I add screenshots.

## What I learned so far
- A database can stay private while the app server reaches it through a security group rule.
- A security group can name another security group as its source.
- PostgreSQL uses TCP 5432.
- Multi-AZ (a standby in another zone) and a snapshot (a backup) solve different problems.
- RDS means I don't install or manage PostgreSQL myself.

## Issue and lesson
Not recorded yet. Lesson from planning: separate network errors (timeout, refused) from login errors (password failed, database missing) before changing anything.

## Mistakes to avoid (for my future projects)
- Making the database public just to get a connection working.
- Publishing the database password or endpoint on GitHub.
- Writing "Multi-AZ" without checking that it was enabled.
- Leaving the RDS instance or snapshot running after the lab.

## Evidence
Screenshots 01 to 05 will go in `screenshots/`.

## Outcome
Documented, not fully confirmed. I'll update this after I check the real results.

## Cost reminder
RDS and EC2 charge by the hour, and Multi-AZ costs more. Delete everything and check Billing.
