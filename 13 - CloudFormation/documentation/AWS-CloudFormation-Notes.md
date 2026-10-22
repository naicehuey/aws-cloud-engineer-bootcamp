# Project 13 — Learning Notes

## Manual setup vs CloudFormation
- **Console (Project 12):** I click through each step. It's easy to forget one and hard to repeat.
- **CloudFormation:** I write the setup in a YAML file and AWS builds it the same way every time.
- A template can go in GitHub, be reviewed, and be reused for other environments.

## Template parts
```yaml
AWSTemplateFormatVersion: '2010-09-09'   # template version
Description: ...
Resources:                               # what to build (required)
Outputs:                                 # values to show after (bucket name, ARN)
```

## My four resources
| Name in template | Type | Purpose |
|---|---|---|
| `LambdaExecutionRole` | `AWS::IAM::Role` | Lets Lambda write logs and read S3 |
| `ProcessingLambdaFunction` | `AWS::Lambda::Function` | Python 3.12 code inside the template |
| `LambdaS3InvokePermission` | `AWS::Lambda::Permission` | Lets S3 call the function |
| `SourceS3Bucket` | `AWS::S3::Bucket` | Receives files and sends the event |

## Intrinsic functions
- `!Ref`: gives a name or ID (for example the bucket name).
- `!GetAtt`: gives an attribute (for example the function's ARN).
- `!Sub`: fills variables into a string, such as `${AWS::AccountId}` and `${AWS::Region}`.
- `DependsOn`: build this resource only after another one exists.

## Why the bucket name uses the account ID and region
S3 bucket names must be unique worldwide. `serverless-processor-data-<account id>-<region>` avoids clashes with other people and earlier tests.

## Circular dependency
```text
Bucket trigger needs -> Lambda permission
Permission needs     -> bucket ARN
```
Solution: the permission builds the bucket ARN from the name with `!Sub`, and the bucket has `DependsOn: LambdaS3InvokePermission`.

## Capabilities
The template creates an IAM role, so the console asks me to tick "I acknowledge that AWS CloudFormation might create IAM resources". Without that the stack can't be created. In the CLI this is `--capabilities CAPABILITY_IAM` (no custom role names here).

## Stack behaviour
- **All or nothing:** if one resource fails, earlier ones are rolled back.
- **ROLLBACK_COMPLETE:** delete the stack before reusing the name.
- **Events tab:** shows the real error under the failed row.
- **Delete stack:** removes everything the stack created. Empty the bucket first.

## Python code in the template
Same as Project 12: checks for S3 `Records`, reads `.json` files with `get_object`, parses them, logs a summary and returns `statusCode: 200`. The handler is `index.lambda_handler` because inline code is saved as `index.py`.

## Commands
```bash
aws cloudformation create-stack \
  --stack-name ServerlessDataProcessorStack \
  --template-body file://template.yaml \
  --capabilities CAPABILITY_IAM
```

## Troubleshooting
```text
Stack failed?  Events tab -> read the CREATE_FAILED reason.
Validation error?  Check property names and types (Architectures is a list).
Name already exists?  Delete the old stack, or use dynamic names.
No logs?  Re-upload the file, wait a few seconds, check the right log group.
```

## Cost awareness
Empty the bucket, delete the stack, then delete the leftover Lambda log group. The log group isn't part of the stack.

## Self-test
1. What is Infrastructure as Code?
2. What does declarative mean?
3. What are `!Ref`, `!GetAtt` and `!Sub`?
4. Why does the S3 trigger need a Lambda permission?
5. Why did I tick the IAM capabilities box?
6. What does rollback do?
7. Why must the bucket be empty before deleting the stack?
8. What stays behind after deleting this stack?

### Answers
1. Describing infrastructure in a file that a tool builds, instead of clicking.
2. I describe the end result and CloudFormation works out the steps.
3. `!Ref` gives a name or ID, `!GetAtt` gives an attribute such as an ARN, `!Sub` substitutes variables into text.
4. Services can't call each other by default, so S3 must be allowed to invoke Lambda.
5. The template creates an IAM role, and CloudFormation requires me to confirm that.
6. It removes what was already created when a step fails, so nothing half-built remains.
7. CloudFormation can't delete a bucket that still holds files.
8. The Lambda log group in CloudWatch.

## One-sentence memory rule
> **A template describes the resources, CloudFormation builds them in the right order, and deleting the stack removes them.**
