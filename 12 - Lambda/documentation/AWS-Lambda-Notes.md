# Project 12 — Learning Notes

## Core flow
```text
File uploaded to S3
      |
      v
S3 sends an event (JSON) --> Lambda runs lambda_handler(event, context)
                                   |
                                   +--> reads the file with boto3 (get_object)
                                   +--> logs to CloudWatch
                                   +--> returns statusCode 200
```

## Concepts

### AWS Lambda
A service that runs my code without me managing a server. It starts when triggered, runs, and stops. I pay for the time it runs.

### Python lambda vs AWS Lambda
- Python `lambda`: a one-line anonymous function inside Python, like `double = lambda x: x * 2`.
- AWS Lambda: the cloud service that runs my code. Only the name is shared.

### Event and JSON
An event is a message saying something happened. AWS sends it as JSON so any language can read it. My function reads two kinds:
- **Manual test event:** `{"test_mode": true, "project": "Serverless-Data-Processor"}`
- **S3 event:** has `Records`, and inside it the bucket name and the object key.

### Handler
`lambda_function.lambda_handler` means: file `lambda_function.py`, function `lambda_handler`. Lambda calls it with `event` (what happened) and `context` (info about the run).

### Trigger
The connection "when X happens, run this function". Mine: S3 `ObjectCreated:*`.

### Execution role (IAM)
The identity the function runs as.
- `AWSLambdaBasicExecutionRole`: write logs to CloudWatch.
- `AmazonS3ReadOnlyAccess`: read files from S3.

### CloudWatch Logs
Where `logger.info(...)` output goes. For my function: `/aws/lambda/<function name>`. Each run has `START`, my log lines, `END` and `REPORT` (with the duration).

### Recursive invocation warning
If a function writes into the same bucket that triggers it, it can loop forever. My function only reads, so it doesn't loop.

## Code explained
| Part | What it does |
|---|---|
| `import boto3` | AWS's Python library, to talk to S3 |
| `logger` | sends messages to CloudWatch |
| `s3_client` | the connection to S3 |
| `if 'Records' in event ...` | decides S3 trigger or manual test |
| `unquote_plus` | turns `my+file%21.json` back into the real file name |
| `get_object` | downloads the file from S3 |
| `json.loads` | turns the text into a Python dictionary |
| `return {...statusCode: 200...}` | the result of the run |
| `except ... raise` | logs the error, then fails the run so Lambda records it |

## Commands and places
- Deploy: the **Deploy** button in the Code tab.
- Manual test: **Test** tab, event name `ManualExecutionTest`, paste `test-event.json`.
- Logs: **Monitor** tab, **View CloudWatch logs**.

## Cost awareness
Lambda has a free tier and costs pennies at this size. Empty and delete the bucket, delete the function and its role when finished.

## Self-test
1. What is AWS Lambda?
2. How is it different from a Python `lambda`?
3. What is an event?
4. What does the handler receive?
5. Why did the function need `AmazonS3ReadOnlyAccess`?
6. Where do I see what the function did?
7. Why is the recursive invocation warning there?
8. How would I make the permission safer?

### Answers
1. A serverless service that runs my code when triggered, without me managing servers.
2. The Python keyword is a tiny function inside code. AWS Lambda is the cloud service.
3. A JSON message saying something happened, such as a file upload.
4. `event` and `context`.
5. To call `get_object` and read the uploaded file.
6. In CloudWatch Logs.
7. A function that writes to its own trigger bucket can loop and run up cost.
8. Use a policy that allows only `s3:GetObject` on this one bucket.

## One-sentence memory rule
> **S3 sends the event, the trigger wakes Lambda, the role decides what Lambda may do, and CloudWatch shows what it did.**
