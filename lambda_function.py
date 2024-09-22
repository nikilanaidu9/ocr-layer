import json
import boto3
import logging

# Initialize S3 client
s3_client = boto3.client('s3')

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Log the event details (for debugging purposes)
    logger.info(f"Received event: {json.dumps(event)}")
    
    # Get the bucket name and object key from the event triggered by S3
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    try:
        # List objects in the bucket after file upload
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        
        # Check if the bucket has files and list them
        if 'Contents' in response:
            files = [item['Key'] for item in response['Contents']]
            logger.info(f"Files in bucket {bucket_name}: {files}")
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': f"Successfully processed {file_key}.",
                    'files': files
                })
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': "No files found in the bucket"
                })
            }

    except Exception as e:
        logger.error(f"Error processing S3 event: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f"Error processing file: {file_key}",
                'error': str(e)
            })
        }
