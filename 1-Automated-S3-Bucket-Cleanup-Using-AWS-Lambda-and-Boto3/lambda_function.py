import boto3
from datetime import datetime, timedelta, timezone

# Initialize the S3 client
s3 = boto3.client('s3')

# Lambda handler function (required for AWS Lambda)
def lambda_handler(event, context):
    # Use your actual bucket name
    bucket_name = 'aditya-serverless-bucket'
    delete_old_objects(bucket_name)

# Function to list and delete objects older than 2 minutes
def delete_old_objects(bucket_name):
    # Get the current time with UTC timezone (aware datetime)
    cutoff_date = datetime.now(timezone.utc) - timedelta(minutes=2)
    
    # List objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)
    
    if 'Contents' in response:
        for obj in response['Contents']:
            obj_name = obj['Key']
            obj_last_modified = obj['LastModified']  # This is an aware datetime
            
            # Check if the object is older than 2 minutes
            if obj_last_modified < cutoff_date:
                # Delete the object
                s3.delete_object(Bucket=bucket_name, Key=obj_name)
                print(f"Deleted object: {obj_name}")
    else:
        print(f"No objects found in the bucket {bucket_name}")
