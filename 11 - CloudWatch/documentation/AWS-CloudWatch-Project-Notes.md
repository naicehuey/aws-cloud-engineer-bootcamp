# Project 11 — Learning Notes

## Four features
- **Metrics:** numbers over time (CPU, memory).
- **Logs:** timestamped events (system messages).
- **Alarms:** rules that change state when a metric crosses a threshold.
- **Dashboards:** pages showing chosen metrics, alarm states and logs.

## EC2 metrics vs agent metrics
- `CPUUtilization` is native to EC2 and is what my alarm uses.
- Memory and disk are collected by the agent and published under `CWAgent`.
- In the console the metrics appear as `mem_used_percent` and `disk_used_percent`.

## IAM
- **Trust policy:** who can use the role (EC2).
- **Permissions policy:** what it can do (`CloudWatchAgentServerPolicy`).
- **Instance profile:** how the role is attached to the instance.
A role that exists but isn't attached does nothing. Use a role, not stored access keys.

## Agent config (`project/cloudwatch-agent-config.json`)
- `metrics_collection_interval: 30`: collect every 30 seconds
- `namespace: CWAgent`: groups the metrics
- `append_dimensions`: adds the instance ID
- `mem` and `disk` with `resources: ["/"]`: memory, and the root disk
- `file_path`, `log_group_name`, `log_stream_name`: which file goes where

## Commands
```bash
sudo dnf install -y amazon-cloudwatch-agent stress-ng
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json -s
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a status
stress-ng --cpu 2 --timeout 120s
```

## Logs
- **Log group:** a container for related logs. Mine: `/aws/ec2/system-messages`.
- **Log stream:** events from one source (this instance).
- **Log event:** one timestamped message.

## Alarm
- Metric: EC2 `CPUUtilization`, greater than 70%, 1-minute period.
- Basic EC2 monitoring may only report every 5 minutes, so check the graph.
- No SNS topic is connected, so no email or SMS is sent.

## Dashboard
CPU chart, memory chart, alarm status, and a logs widget. Useful to compare a CPU spike with memory and log messages.

## Troubleshooting
```text
No metrics?  agent running? role attached? right region? namespace CWAgent? wait a few minutes.
No logs?     /var/log/messages exists? path and group name right? permissions?
No alarm?    right instance and metric? threshold and period? did the load really raise CPU?
Blank dashboard? region, dimensions, time range.
```

## Cost awareness
EC2, metric ingestion, log storage, dashboards and alarms can charge. Delete the dashboard, alarm, log group and EC2 server after saving evidence.

## Self-test
1. How do metrics and logs differ?
2. Why does this lab use an agent for memory?
3. What does an EC2 instance role do?
4. What does the 70% threshold mean?
5. Why might a 2-minute stress test not trigger the alarm?
6. How does the dashboard help troubleshooting?
7. What do I check first if `CWAgent` metrics stop?

### Answers
1. Metrics are numbers over time. Logs are text events.
2. EC2 doesn't report memory by itself.
3. It gives the server permissions without stored keys.
4. The alarm goes to In alarm when CPU stays above 70% for the evaluated period.
5. CloudWatch evaluates datapoints over time, and basic monitoring reports slowly.
6. It shows CPU, memory, alarm state and logs together.
7. Agent status, then the role, region and namespace.

## One-sentence memory rule
> **EC2 gives CPU, the agent adds memory, disk and logs, the alarm watches CPU, and the dashboard puts it all on one page.**
