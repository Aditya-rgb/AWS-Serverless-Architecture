import boto3
from datetime import datetime, timedelta, timezone

def lambda_handler(event, context):
    # Initialize the S3 client
    s3 = boto3.client('s3')
    bucket_name = 'aditya-serverless-bucket'  # Replace with your bucket name

    # Define the cutoff date (90 days ago)
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=90)

    # List objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    # Check if the bucket has objects
    if 'Contents' in response:
        for obj in response['Contents']:
            obj_key = obj['Key']
            obj_last_modified = obj['LastModified']

            # Check if the object is a log file and older than 90 days
            if obj_key.endswith('.log') and obj_last_modified < cutoff_date:
                # Delete the old log file
                s3.delete_object(Bucket=bucket_name, Key=obj_key)

                # Log the deletion
                print(f"Deleted old log file: {obj_key}")

    else:
        print(f"No objects found in the bucket {bucket_name}")

    return {
        'statusCode': 200,
        'body': 'Old log cleanup completed successfully'
    }
