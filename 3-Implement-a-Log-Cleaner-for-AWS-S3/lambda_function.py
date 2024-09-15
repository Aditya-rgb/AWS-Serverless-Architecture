import boto3
from datetime import datetime, timedelta, timezone

def lambda_handler(event, context):
    # The S3 client was set up to communicate with Amazon S3
    s3 = boto3.client('s3')
    
    # The bucket name where the files were stored was specified
    bucket_name = 'aditya-serverless-bucket'  # Replace with your bucket name

    # The cutoff time was set to 5 minutes ago from the current time
    cutoff_date = datetime.now(timezone.utc) - timedelta(minutes=5)

    # A request was made to list all the files in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    # It was checked whether there were any files in the bucket
    if 'Contents' in response:
        # If files were found, each one was checked
        for obj in response['Contents']:
            obj_key = obj['Key']  # The name (key) of the file was noted
            obj_last_modified = obj['LastModified']  # The last time the file was changed was noted

            # It was checked if the file was a log file and if it was older than 5 minutes
            if obj_key.endswith('.log') and obj_last_modified < cutoff_date:
                # The old log file was deleted
                s3.delete_object(Bucket=bucket_name, Key=obj_key)

                # A message was printed to confirm that the log file was deleted
                print(f"Deleted old log file: {obj_key}")

    else:
        # If no files were found in the bucket, a message was printed
        print(f"No objects found in the bucket {bucket_name}")

    # A success message was returned after the cleanup was completed
    return {
        'statusCode': 200,
        'body': 'Log cleanup completed successfully'
    }
