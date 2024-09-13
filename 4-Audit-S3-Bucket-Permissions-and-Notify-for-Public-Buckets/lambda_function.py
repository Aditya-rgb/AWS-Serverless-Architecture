import boto3
import json

# Initialize Boto3 client for S3
s3_client = boto3.client('s3')

def check_bucket_permissions(bucket_name):
    try:
        # Get the bucket ACL
        acl = s3_client.get_bucket_acl(Bucket=bucket_name)
        for grant in acl['Grants']:
            grantee = grant['Grantee']
            permission = grant['Permission']
            
            # Check if the bucket is public (has 'AllUsers' group with read/write permissions)
            if grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                if permission in ['READ', 'WRITE']:
                    return True
        return False
    except Exception as e:
        print(f"Error checking bucket permissions for {bucket_name}: {e}")
        return False

def lambda_handler(event, context):
    try:
        # List all S3 buckets
        response = s3_client.list_buckets()
        buckets = response['Buckets']
        
        # Print all bucket names to CloudWatch logs
        print("All buckets for audit:")
        for bucket in buckets:
            print(bucket['Name'])
        
        public_buckets = []
        
        for bucket in buckets:
            bucket_name = bucket['Name']
            if check_bucket_permissions(bucket_name):
                public_buckets.append(bucket_name)
                
        if public_buckets:
            # Log the public buckets
            print(f"Public buckets: {public_buckets}")
            return {
                'statusCode': 200,
                'body': json.dumps(f"Public buckets: {public_buckets}")
            }
        else:
            print("No public buckets found.")
            return {
                'statusCode': 200,
                'body': json.dumps("No public buckets found.")
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error occurred: {e}")
        }
