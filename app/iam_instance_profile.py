from os import environ, getenv
from botocore.exceptions import ClientError


class IAMInstanceProfile:
    def create(session):
        iam = session.client('iam')
        try:
            response = iam.create_instance_profile(
                InstanceProfileName=getenv("INSTANCE_PROFILE_NAME")
            )
            instance_profile_arn = response['InstanceProfile']['Arn']
            
            environ['INSTANCE_PROFILE_ARN'] = instance_profile_arn

            print(f"IAM Instance Profile {instance_profile_arn} Created!")

            # Adding Role to Instance Profile
            response = iam.add_role_to_instance_profile(
                InstanceProfileName=getenv("INSTANCE_PROFILE_NAME"),
                RoleName=getenv("ROLE_NAME")
            )
            print(f"IAM Role {getenv('ROLE_NAME')} added to Instance Profile {getenv('INSTANCE_PROFILE_NAME')}")

        except ClientError as e:
            print(f'\n\nError in IAMInstanceProfile File\n{e}')
