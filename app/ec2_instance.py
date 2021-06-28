from os import getenv
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
        # Create Security Group
        # SecurityGroup.create(session)
        # sleep(2)
        print(f"user_data init: {self.user_data}")
        ec2 = self.session.client('ec2')

        try:
            ec2.run_instances(
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

        except ClientError as e:
            print(f'\n\nError in EC2Instance File\n{e}')
