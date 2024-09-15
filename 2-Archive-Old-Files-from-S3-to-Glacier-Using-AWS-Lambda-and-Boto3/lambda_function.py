import boto3
from datetime import datetime, timedelta, timezone

# The S3 client was set up to communicate with Amazon S3
s3 = boto3.client('s3')

# The main function for AWS Lambda was defined, which gets triggered when the Lambda runs
def lambda_handler(event, context):
    # The bucket name was specified where the images were stored
    bucket_name = 'aditya-serverless-bucket'
    # A function was called to move old objects to Glacier
    move_old_objects_to_glacier(bucket_name)

# This function found and moved any files in the bucket that were older than 5 minutes
def move_old_objects_to_glacier(bucket_name):
    # The current date and time were noted, adjusting for UTC and subtracting 5 minutes
    cutoff_date = datetime.now(timezone.utc) - timedelta(minutes=5)
    
    # A request was made to Amazon S3 to list all the files in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)
    
    # If the bucket had files, each file was checked
    if 'Contents' in response:
        for obj in response['Contents']:
            obj_name = obj['Key']  # The name of the file was extracted
            obj_last_modified = obj['LastModified']  # The last time the file was modified was noted
            
            # It was checked if the file was last modified more than 5 minutes ago - For real user world edge case change 5 minuts to 6 months
            if obj_last_modified < cutoff_date:
                # The file was moved to Amazon Glacier for long-term storage
                s3.copy_object(
                    Bucket=bucket_name,
                    CopySource={'Bucket': bucket_name, 'Key': obj_name},
                    Key=obj_name,
                    StorageClass='GLACIER'
                )
                print(f"Moved object: {obj_name} to Glacier")  # A message was printed showing which file was moved
    else:
        # If no files were found, a message was printed
        print(f"No objects found in the bucket {bucket_name}")
