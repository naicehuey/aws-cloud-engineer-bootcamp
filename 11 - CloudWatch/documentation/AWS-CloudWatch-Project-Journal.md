# Project 11 — Project Journal

**Date:** Not recorded

## Goal
See what my EC2 server is doing (CPU, memory, disk, system log) and get an alarm when CPU is high.

## Work completed
- Documentation, agent config and commands are written.
- The build steps are to confirm once I add screenshots.

## What I learned so far
- CloudWatch has four parts I used: metrics, logs, alarms and dashboards.
- EC2 reports CPU itself. Memory and disk need the CloudWatch agent.
- A server needs an IAM role to send data, and the role must be attached to the instance.
- An alarm only changes state unless I connect it to something like SNS.
- A short load test doesn't always trigger an alarm because CloudWatch evaluates data over time.

## Milestones
| Milestone | Status |
|---|---|
| IAM role and instance profile | To confirm |
| EC2 server running | To confirm |
| Agent installed and running | To confirm |
| Memory and disk metrics in `CWAgent` | To confirm |
| Log events in `/aws/ec2/system-messages` | To confirm |
| CPU alarm created | To confirm |
| Load test and alarm result | To confirm |
| Dashboard saved | To confirm |
| Cleanup | To confirm |

## Issue and lesson
Not recorded yet. If something fails, I'll write the symptom, the cause and the fix. Useful checks: agent status, the role attached, the region, and the log file path.

## Mistakes to avoid (for my future projects)
- Saying an alarm triggered without seeing "In alarm" in a screenshot.
- Claiming notifications when no SNS topic is connected.
- Leaving the EC2 server, dashboard and log group behind.
- Putting access keys on a server instead of using a role.

## Evidence
Screenshots 01 to 05 will go in `screenshots/`.

## Outcome
Documented, not fully confirmed. I'll update this after I check the real results.

## Cost reminder
EC2 runtime, log storage, dashboards and alarms can cost money. Delete them after saving evidence and check Billing.
