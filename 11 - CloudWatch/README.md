# Project 11 — Monitoring an EC2 Server with CloudWatch

## Overview
My first project with Amazon CloudWatch. I set up an EC2 server to send its memory use, disk use and system log to CloudWatch, added an alarm for high CPU, and planned a dashboard to see it all in one place. I'm still learning CloudWatch, so this README records the plan and what I have evidence for so far.

> **Status:** documentation and the agent config are ready. Everything marked "to confirm" needs my screenshots and results before I treat it as done.

## Stack
Amazon CloudWatch (Metrics, Logs, Alarms, Dashboards) · Unified CloudWatch Agent · Amazon EC2 (Amazon Linux 2023) · AWS IAM · AWS Management Console

## What I practiced
- Giving an EC2 server an IAM role so the agent can send data without access keys
- Installing and configuring the CloudWatch agent
- Reading memory and disk metrics in the `CWAgent` namespace
- Sending a system log file to CloudWatch Logs
- Creating a CPU alarm and testing it with a load tool
- Building a dashboard

## Configuration (plan)
| Item | Value |
|---|---|
| EC2 name | `Monitored-App-Server` |
| OS / type | Amazon Linux 2023, `t3.micro` |
| IAM role | `EC2-CloudWatch-Monitoring-Role` with `CloudWatchAgentServerPolicy` |
| Metrics namespace | `CWAgent` (`mem_used_percent`, disk `used_percent` for `/`) |
| Log group | `/aws/ec2/system-messages` (from `/var/log/messages`) |
| Alarm | `EC2-High-CPU-Utilization-Alarm`, CPU greater than 70%, 1-minute period |
| Dashboard | `EC2-System-Observability-Dashboard` |

## Project structure
```text
11-cloudwatch/
├── project/
│   ├── cloudwatch-agent-config.json   # agent configuration
│   └── commands.sh                    # commands I ran, in order
├── documentation/
│   ├── CloudWatch-Journal.md
│   └── CloudWatch-Notes.md
├── architecture/
│   └── CloudWatch-Architecture-Diagram.md
├── screenshots/
│   ├── 01-cloudwatch-agent-active.png
│   ├── 02-cloudwatch-custom-metrics.png
│   ├── 03-cloudwatch-log-stream.png
│   ├── 04-cloudwatch-alarm-triggered.png
│   └── 05-cloudwatch-dashboard.png
└── README.md
```

## Architecture
```text
EC2 (Amazon Linux 2023, IAM role attached)
        |
CloudWatch Agent
   |            |
memory + disk   /var/log/messages
   |            |
   v            v
+-----------------------------+
|        CloudWatch           |
| Metrics | Logs | Alarm      |   (CPU comes from EC2 itself)
+--------------+--------------+
               |
          Dashboard
```

## Screenshots
Add these after hiding account IDs and public IPs. Only add the alarm screenshot if the alarm really went into "In alarm".

1. `01-cloudwatch-agent-active.png` — agent status running
2. `02-cloudwatch-custom-metrics.png` — memory and disk metrics in `CWAgent`
3. `03-cloudwatch-log-stream.png` — log events in the log group
4. `04-cloudwatch-alarm-triggered.png` — alarm state and CPU graph
5. `05-cloudwatch-dashboard.png` — the saved dashboard

## What I did (plan)
1. Create the IAM role and attach `CloudWatchAgentServerPolicy`. (to confirm)
2. Launch `Monitored-App-Server` with that role. (to confirm)
3. Install the agent and `stress-ng` (`project/commands.sh`). (to confirm)
4. Save `cloudwatch-agent-config.json` on the server and start the agent. (to confirm)
5. Check memory, disk and log data in CloudWatch. (to confirm)
6. Create the CPU alarm and run `stress-ng --cpu 2 --timeout 120s`. (to confirm)
7. Build the dashboard. (to confirm)
8. Delete the dashboard, alarm, log group and EC2 server. (to confirm)

## Key ideas (in my own words)
- **Metrics** are numbers over time (CPU, memory). **Logs** are text events.
- **Alarm:** a rule on a metric that changes state, for example OK to In alarm.
- **Dashboard:** one page showing the charts and alarm state I care about.
- **Why an agent:** EC2 reports CPU by itself, but not memory or disk. The agent collects those.
- **IAM role:** lets the server send data to CloudWatch without keeping access keys on it.

My one-sentence rule: **EC2 gives CPU, the agent adds memory, disk and logs, the alarm watches CPU, and the dashboard puts it all on one page.**

## Challenge
Not recorded yet. I'll add what went wrong and how I fixed it.

## Validation checklist
- [ ] Role attached to the instance
- [ ] Agent shows running
- [ ] `CWAgent` memory and disk metrics visible
- [ ] Log events visible in `/aws/ec2/system-messages`
- [ ] Alarm created
- [ ] Alarm went to "In alarm" during the load test (only if it did)
- [ ] Dashboard saved with data in the widgets
- [ ] Resources deleted

## Notes
- **No notification yet.** My steps don't connect an SNS topic, so the alarm only changes state. It doesn't send an email or SMS. I won't say "automated alerting" unless I add that. The original project title says it, so I use "Monitoring and alarms" instead.
- **One-minute alarm:** as far as I know, EC2's basic monitoring reports CPU every 5 minutes, so a 1-minute alarm may show "Insufficient data" unless detailed monitoring is on (which costs extra). A 2-minute stress test may also not be enough to trigger it. I'll check the graph before I claim it triggered.
- **Log file:** as far as I know, Amazon Linux 2023 doesn't have `/var/log/messages` by default, because it logs to the journal. If the log group stays empty, I'll check that the file exists, for example by installing `rsyslog`.
- **Disk metric name:** it appears in the console as `disk_used_percent`. I'll confirm it in my screenshot.
- Cost: the EC2 server, log storage, dashboards and alarms can charge. I delete them after saving evidence and check Billing.

Documentation was written with AI assistance (Claude) for structure and clarity. I do the labs in the AWS Console myself and check what is written here against what I did.
