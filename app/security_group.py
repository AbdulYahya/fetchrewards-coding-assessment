from os import environ
from botocore.exceptions import ClientError


class SecurityGroup:
    def create(session):
        ec2 = session.client('ec2')
        response = ec2.describe_vpcs()

        vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

        try:
            response = ec2.create_security_group(GroupName='Assessment_SG',
                                                 Description='Assessment SG',
                                                 VpcId=vpc_id)
            security_group_id = response['GroupId']
            print(f"Security Group Created {security_group_id} \
                    in VPC {vpc_id}")

            # Store the Security Group's ID in an environment variable
            environ["AWS_SECURITY_GROUP_ID"] = security_group_id

            data = ec2.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }
                ])
            print(f"Ingress Successfully Set {data}")

        except ClientError as e:
            print(f'\n\nError in SecurityGroup File:\n{e}')

