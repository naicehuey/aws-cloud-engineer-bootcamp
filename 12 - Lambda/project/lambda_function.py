import json
import logging
import datetime
import urllib.parse
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    execution_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    logger.info(f"=== LAMBDA EXECUTION STARTED AT {execution_time} ===")
    logger.info(f"Raw Input Event: {json.dumps(event)}")

    try:
        # S3 Trigger Event Branch
        if 'Records' in event and len(event['Records']) > 0 and 's3' in event['Records'][0]:
            s3_record = event['Records'][0]['s3']
            bucket_name = s3_record['bucket']['name']
            file_key = urllib.parse.unquote_plus(s3_record['object']['key'], encoding='utf-8')
            file_size = s3_record['object'].get('size', 0)

            logger.info(f"[S3 TRIGGER DETECTED] File: {file_key} | Bucket: {bucket_name} | Size: {file_size} bytes")

            if file_key.endswith('.json'):
                response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
                content = response['Body'].read().decode('utf-8')
                data = json.loads(content)
                logger.info(f"File content parsed successfully: {data}")

            response_body = {
                "status": "S3 Event Processed Successfully",
                "bucket": bucket_name,
                "file": file_key,
                "timestamp": execution_time
            }

        # Manual Test Branch
        else:
            logger.info("Manual invocation payload received.")
            response_body = {
                "status": "Manual Execution Processed",
                "received_payload": event,
                "timestamp": execution_time
            }

        logger.info(f"Execution Summary: {json.dumps(response_body)}")
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response_body)
        }

    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        raise e
