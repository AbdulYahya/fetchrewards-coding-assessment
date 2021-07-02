from os import environ, getenv
from botocore.exceptions import ClientError


class EC2Instance:
    def __init__(self, config, session):
        self.config = config['server']
        self.session = session

        with open('./user_data_ci.txt', 'r') as file:
            filedata = file.read()
            filedata = filedata.replace('$USER1_SSH_PUBLIC_KEY',
                                        getenv('USER1_SSH_PUBLIC_KEY'))
            filedata = filedata.replace('$USER2_SSH_PUBLIC_KEY',
                                        getenv('USER2_SSH_PUBLIC_KEY'))
            self.user_data = filedata

    def launch(self):
        volumes = self.config['volumes']
        ec2 = self.session.client('ec2')

        try:
            response = ec2.run_instances(
                BlockDeviceMappings=[
                    {
                        'DeviceName': volumes[0]['device'],
                        'Ebs': {
                            'VolumeSize': volumes[0]['size_gb'],
                        },
                    },
                    {
                        'DeviceName': volumes[1]['device'],
                        'Ebs': {
                            'VolumeSize': volumes[1]['size_gb'],
                        },
                    },
                ],
                ImageId=getenv("AWS_L2_AMI_ID"),
                InstanceType=self.config['instance_type'],
                KeyName='root_key',
                MaxCount=self.config['max_count'],
                MinCount=self.config['min_count'],
                Monitoring={
                    'Enabled': True
                },
                SecurityGroupIds=[
                    getenv('AWS_SECURITY_GROUP_ID')
                ],
                SubnetId="subnet-c25789ba",
                UserData=self.user_data,
            )

            instance_id = response['Instances'][0]['InstanceId']
            print(f"EC2 Instance {instance_id} Launched Successfully!")
            
            self.instance_id = instance_id
            
        except ClientError as e:
            print(f'\n\nError in EC2Instance File\n{e}')
    
    def attach_profile(self):
            ec2 = self.session.client('ec2')

            waiter = ec2.get_waiter('instance_running')
            
            print("\n\nWaiting for EC2 instance 'Running' state...\nPolling EC2 every 10 seconds...\n")
            print("Thank you for your patience")
            waiter.wait(InstanceIds=[
                self.instance_id
            ])
            
            print(f"\nEC2 Instance {self.instance_id} is now running!")
            print("\nAssociating IAM Instance Profile")
                   
            # Associate Instance Profile with EC2 Instance
            ec2.associate_iam_instance_profile(
                IamInstanceProfile={
                    'Arn': getenv('INSTANCE_PROFILE_ARN'),
                    'Name': getenv('INSTANCE_PROFILE_NAME')
                },
                InstanceId=self.instance_id
            )
            print(f"\nInstance Profile {getenv('INSTANCE_PROFILE_ARN')}" + 
                "Successfully Associated with EC2 Instance {self.instance_id}")

    def get_instance_id(self):
        return self.instance_id
                    