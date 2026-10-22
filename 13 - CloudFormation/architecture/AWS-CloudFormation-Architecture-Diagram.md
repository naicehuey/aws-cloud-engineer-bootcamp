# Project 13 — Architecture

```
+------------------------- CloudFormation stack ---------------------------+
|                    ServerlessDataProcessorStack                          |
|                                                                          |
|   User / me                                                              |
|      |  1. upload sample-payload.json                                    |
|      v                                                                   |
|  +----------------------+   2. s3:ObjectCreated:\*   +------------------+ |
|  | S3 bucket            | ------------------------> | Lambda function  | |
|  | SourceS3Bucket       | <----- 3. get\_object ---- | Python 3.12      | |
|  +----------+-----------+                           +---------+--------+ |
|             ^                                                 |          |
|             | allowed by                                      | 4. logs  |
|  +----------+-----------+                                     v          |
|  | Lambda permission    |                          +------------------+  |
|  | LambdaS3Invoke       |                          | CloudWatch Logs  |  |
|  | Permission           |                          | (outside stack)  |  |
|  +----------------------+                          +------------------+  |
|                                                                          |
|  +----------------------+                                                |
|  | IAM execution role   |  used by the Lambda function                   |
|  | LambdaExecutionRole  |  (logs + S3 read)                              |
|  +----------------------+                                                |
+--------------------------------------------------------------------------+
```

|Name in template|Type|Purpose|
|-|-|-|
|`SourceS3Bucket`|`AWS::S3::Bucket`|Receives files and sends the event|
|`ProcessingLambdaFunction`|`AWS::Lambda::Function`|Processes the uploaded file|
|`LambdaExecutionRole`|`AWS::IAM::Role`|Permissions for logs and S3 read|
|`LambdaS3InvokePermission`|`AWS::Lambda::Permission`|Lets S3 invoke the function|
|CloudWatch log group|Created by Lambda|Not part of the stack|



