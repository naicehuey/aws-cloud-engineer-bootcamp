# Project 13 — Project Journal

**Date:** October 7, 2026

## Goal
Rebuild my S3 to Lambda to CloudWatch pipeline from Project 12 as Infrastructure as Code, so one file can create it all.

## Work completed
1. Wrote the template with four resources: IAM role, Lambda function, Lambda permission, S3 bucket with trigger.
2. Created the stack `ServerlessDataProcessorStack` and ticked the IAM capabilities box.
3. Fixed the failed attempts (see below) until the stack reached CREATE_COMPLETE.
4. Checked Outputs and Resources.
5. Uploaded `sample-payload.json` to the new bucket.
6. Found the Lambda run in the log group: trigger detected, JSON parsed, summary written.

## What I learned
- CloudFormation builds resources in the right order and removes them all when I delete the stack.
- A template is declarative: I describe the end result.
- `!Ref` gives a name or ID, `!GetAtt` gives an attribute like an ARN, `!Sub` fills in variables like the account ID and region.
- Using the account ID and region in the bucket name avoids name clashes.
- An S3 trigger needs permission for S3 to call the Lambda, and that is a separate resource.
- Rollback keeps the account clean by removing partly built stacks.

## Issue and lesson
- **Rollback and validation failures.** Early attempts failed, including a "1 Deployment validations failed" message. The fix that worked was changing `Architecture` to `Architectures` as a list. I didn't write down the exact first error, so I can't say for sure it was the cause of every failure. Lesson: open the Events tab, copy the exact error, and save it.
- **Reusing a stack name.** A stack in `ROLLBACK_COMPLETE` must be deleted before the name can be used again.
- **Circular dependency.** I built the bucket ARN with `!Sub` for the Lambda permission and used `DependsOn` on the bucket, so the resources don't wait on each other forever.
- **Finding the logs.** The CloudWatch menu had changed (Log Management, then Log groups). The "View CloudWatch logs" button on the Lambda Monitor tab is a shortcut.

## Mistakes to avoid (for my future projects)
- Guessing the cause of a failure without reading the Events tab.
- Copying a template from a chat without checking property names.
- Deleting the stack before emptying the bucket.
- Forgetting the log group, which stays after the stack is gone.
- Claiming "least privilege" with a broad managed policy.

## Evidence
Screenshots 01 to 04: stack CREATE_COMPLETE, stack resources, JSON file in S3, log events in CloudWatch.

## Outcome
A working pipeline created entirely from one template. Next I want to try a parameter or two, update a stack with a change, and use a narrower policy.

## Cost reminder
Costs are small, but I delete the stack after the lab (empty the bucket first) and remove the leftover log group.
