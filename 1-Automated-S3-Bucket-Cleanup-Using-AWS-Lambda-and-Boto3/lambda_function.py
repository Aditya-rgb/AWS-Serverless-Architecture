import boto3
from datetime import datetime, timedelta, timezone

# The S3 client was initialized using Boto3
s3 = boto3.client('s3')

# The Lambda handler function, required for AWS Lambda, was defined
def lambda_handler(event, context):
    # The actual bucket name was used
    bucket_name = 'aditya-serverless-bucket'
    delete_old_objects(bucket_name)

# The function listed and deleted objects older than 2 minutes
def delete_old_objects(bucket_name):
    # The current time was obtained with UTC timezone (aware datetime)
    cutoff_date = datetime.now(timezone.utc) - timedelta(minutes=2)
    
    # The objects in the bucket were listed
    response = s3.list_objects_v2(Bucket=bucket_name)
    
    if 'Contents' in response:
        for obj in response['Contents']:
            obj_name = obj['Key']
            obj_last_modified = obj['LastModified']  # This was an aware datetime
            
            # The function checked if the object was older than 2 minutes
            # For testing purposes i took 2 minutes, you can tweak the code and make it 30 days too.. :)
            if obj_last_modified < cutoff_date:
                # The object was deleted
                s3.delete_object(Bucket=bucket_name, Key=obj_name)
                print(f"Deleted object: {obj_name}")
    else:
        # It printed that no objects were found in the bucket
        print(f"No objects found in the bucket {bucket_name}")
