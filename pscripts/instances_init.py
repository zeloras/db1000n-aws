import boto3
import botocore

ec2 = boto3.resource('ec2')
ec2_client = boto3.client('ec2')
security_group = None

for instance in ec2.instances.all():
    if instance.state['Name'] == 'running':
        security_group = instance.security_groups[0]['GroupId']


try:
    update_security_group = ec2_client.authorize_security_group_ingress(
        GroupId=security_group,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]
    )
except botocore.exceptions.ClientError:
    print("Probably security rule already exists")
