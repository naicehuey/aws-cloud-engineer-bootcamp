                      [ Amazon EC2 Instance ]
                     (App Server / Linux 2023)
                                │
                 ┌──────────────┴──────────────┐
                 │  Unified CloudWatch Agent   │
                 └──────────────┬──────────────┘
                                │ (OS Metrics & Logs)
                                ▼
                       [ Amazon CloudWatch ]
         ┌──────────────────────┼──────────────────────┐
         ▼                      ▼                      ▼
  [ Log Groups ]        [ Custom Metrics ]     [ CloudWatch Alarms ]
 (/var/log/messages)   (RAM & Disk Usage)     (High CPU Trigger > 70%)
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                ▼
                   [ CloudWatch Dashboard ]