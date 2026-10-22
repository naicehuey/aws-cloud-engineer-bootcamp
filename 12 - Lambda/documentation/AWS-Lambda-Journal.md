# Project 12 — Project Journal

**Date:** October 7, 2026 (first attempt earlier that week)

## Goal
Build a pipeline where uploading a file to S3 automatically runs a Python function and records the result in CloudWatch.

## Work completed
1. Created the Lambda function (Python 3.12).
2. Attached `AmazonS3ReadOnlyAccess` to its role, next to the logging policy.
3. Deployed `lambda_function.py` and ran the manual test event, which returned `statusCode: 200`.
4. Created the bucket `serverless-data-processor-huey-2026`.
5. Added the S3 trigger (all object create events).
6. Uploaded `sample-data.json`.
7. Checked CloudWatch Logs: the function ran by itself, found my file, parsed it and finished in about 292 ms.

## What I learned
- A Lambda function only runs when something triggers it, and I pay for use rather than for a server sitting idle.
- The handler gets an **event**. For S3 it contains the bucket name and file name. For my manual test it was just the JSON I typed.
- The same code can handle both cases by checking if the event has `Records`.
- The function's IAM role decides what it is allowed to do. Logs need one policy, reading S3 needs another.
- CloudWatch Logs is the only way to see what a serverless function did.
- Python's `lambda` keyword and AWS Lambda are different things.

## Issue and lesson
**Where does the test JSON go?** I looked under Runtime settings and Layers, but the test event belongs in the **Test** tab. Lesson: read the tab names first, and don't trust an instruction word for word when the console has changed.

**Messy restart.** After my first failed attempt the new function kept details from the old one and Deploy complained. I deleted the function, the IAM role and the bucket and started again. Lesson: clean up fully before restarting.

**Function name.** My later screenshots show the function as `Serverless-Data-Processor-role`, not `Serverless-Data-Processor`. I'm not sure if I typed it that way when I recreated it. Lesson: check names as I type them, because the log group takes its name from the function.

## Mistakes to avoid (for my future projects)
- Searching random Edit buttons instead of reading the tabs.
- Leaving old resources around when I restart a lab.
- Giving a role a broad policy when a narrow one would do.
- Posting screenshots that show the account ID.

## Evidence
Screenshots 01 to 04: function and runtime, code with the passed manual test, S3 trigger on the function overview, and the CloudWatch log lines for the S3 run.

## Outcome
A working serverless pipeline. Next time I want to scope the permission to one bucket, handle bad JSON on purpose, and try a trigger from a different service.

## Cost reminder
Lambda and S3 cost very little at this size, but I delete the bucket and function after the project and check Billing.
