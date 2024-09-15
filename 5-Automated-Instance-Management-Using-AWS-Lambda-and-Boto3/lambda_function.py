import boto3

# The EC2 client was initialized to interact with AWS EC2 services
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    try:
        # The EC2 instances tagged with 'Action: Auto-Stop' were stopped
        stop_instances()

        # The EC2 instances tagged with 'Action: Auto-Start' were started
        start_instances()
    except Exception as e:
        # Any errors that occurred were printed
        print(f"Error occurred: {e}")

def stop_instances():
    try:
        # It gathered all EC2 instances with the tag 'Action: Auto-Stop' that were currently running
        instances_to_stop = ec2.describe_instances(
            Filters=[
                {
                    'Name': 'tag:Action',
                    'Values': ['Auto-Stop']
                },
                {
                    'Name': 'instance-state-name',
                    'Values': ['running']
                }
            ]
        )

        # The instance IDs were extracted and the instances were stopped
        for reservation in instances_to_stop['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']  # The instance ID was retrieved
                name = get_instance_name(instance)  # The name tag (if present) was fetched
                print(f"Stopping instance: {instance_id}, Name: {name}")
                ec2.stop_instances(InstanceIds=[instance_id])  # The instance was stopped
    except Exception as e:
        # Any errors during stopping were logged
        print(f"Error stopping instances: {e}")

def start_instances():
    try:
        # It gathered all EC2 instances with the tag 'Action: Auto-Start' that were currently stopped
        instances_to_start = ec2.describe_instances(
            Filters=[
                {
                    'Name': 'tag:Action',
                    'Values': ['Auto-Start']
                },
                {
                    'Name': 'instance-state-name',
                    'Values': ['stopped']
                }
            ]
        )

        # The instance IDs were extracted and the instances were started
        for reservation in instances_to_start['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']  # The instance ID was retrieved
                name = get_instance_name(instance)  # The name tag (if present) was fetched
                print(f"Starting instance: {instance_id}, Name: {name}")
                ec2.start_instances(InstanceIds=[instance_id])  # The instance was started
    except Exception as e:
        # Any errors during starting were logged
        print(f"Error starting instances: {e}")

def get_instance_name(instance):
    # The 'Name' tag was searched for in the instance's tags
    for tag in instance.get('Tags', []):
        if tag['Key'] == 'Name':
            return tag['Value']
    # If no 'Name' tag was found, it returned 'Unnamed Instance'
    return 'Unnamed Instance'
