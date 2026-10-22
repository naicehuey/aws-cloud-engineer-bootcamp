# Project 09 — Project Journal

**Date:** Not recorded

## Goal
Make a website that switches to a backup page by itself when the main server stops answering.

## Work completed
- Built the S3 backup page (`index.html`).
- The rest of the build (EC2, hosted zone, health check, failover records, outage test) is to confirm once I add screenshots.

## What I learned so far
- Failover is a DNS decision: Route 53 returns a different answer when the health check says Unhealthy.
- The health check only reports health. It doesn't restart anything.
- A backup page on S3 is a cheap way to show visitors a maintenance message.
- DNS caching (TTL) means visitors may not switch the moment the server fails.

## Issue and lesson
Not recorded yet. If I hit problems (unhealthy check, wrong record name, S3 page not loading), I'll write the exact symptom and fix here.

## Mistakes to avoid (for my future projects)
- Pointing the health check at an IP that changes when the instance restarts.
- Leaving EC2, the health check or the hosted zone running after the lab.
- Writing results before I have tested them.

## Evidence
Screenshots 01 to 05 will go in `screenshots/`.

## Outcome
Partly built. I'll update this when the failover test is done.

## Cost reminder
Hosted zone, health check and EC2 all cost money while they exist. Delete them after testing and check Billing.
