#!/bin/bash
# Commands from Project 11 (run on the EC2 instance, one by one)

sudo dnf update -y
sudo dnf install -y amazon-cloudwatch-agent stress-ng

# copy cloudwatch-agent-config.json to this path first
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config -m ec2 \
  -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json -s

# check the agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a status

# CPU load test (2 minutes)
stress-ng --cpu 2 --timeout 120s
