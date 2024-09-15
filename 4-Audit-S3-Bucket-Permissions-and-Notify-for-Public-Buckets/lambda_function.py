import boto3
import json

# The S3 client was initialized using Boto3 to interact with S3 services
s3_client = boto3.client('s3')

# This function checked the permissions of a specified S3 bucket
def check_bucket_permissions(bucket_name):
    try:
        # The ACL (Access Control List) of the bucket was retrieved
        acl = s3_client.get_bucket_acl(Bucket=bucket_name)
        
        # It went through the permissions set for the bucket
        for grant in acl['Grants']:
            grantee = grant['Grantee']
            permission = grant['Permission']
            
            # The function checked if the bucket was public by looking for the 'AllUsers' group with read/write permissions
            if grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                if permission in ['READ', 'WRITE']:
                    # If public access was found, it returned True
                    return True
        # If no public access was found, it returned False
        return False
    except Exception as e:
        # In case of an error, it printed a message and returned False
        print(f"Error checking bucket permissions for {bucket_name}: {e}")
        return False

# The main Lambda handler function was defined
def lambda_handler(event, context):
    try:
        # A list of all the S3 buckets was requested
        response = s3_client.list_buckets()
        buckets = response['Buckets']
        
        # It printed the names of all the buckets to CloudWatch logs for auditing
        print("All buckets for audit:")
        for bucket in buckets:
            print(bucket['Name'])
        
        # An empty list was created to store the names of public buckets
        public_buckets = []
        
        # Each bucket was checked to see if it was public
        for bucket in buckets:
            bucket_name = bucket['Name']
            if check_bucket_permissions(bucket_name):
                # If a bucket was public, it was added to the list
                public_buckets.append(bucket_name)
                
        if public_buckets:
            # If public buckets were found, they were logged and returned in the response
            print(f"Public buckets: {public_buckets}")
            return {
                'statusCode': 200,
                'body': json.dumps(f"Public buckets: {public_buckets}")
            }
        else:
            # If no public buckets were found, a message was logged and returned
            print("No public buckets found.")
            return {
                'statusCode': 200,
                'body': json.dumps("No public buckets found.")
            }
    except Exception as e:
        # In case of an error, it returned a message with the error details
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error occurred: {e}")
        }
