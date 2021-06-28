from os import environ, getenv
import json
from botocore.exceptions import ClientError


class IAMRole:
    def create(session):
        assumeRolePolicyDocument = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ec2.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }

        iam = session.client('iam')
        try:
            response = iam.create_role(
                Path=getenv("ROLE_PATH"),
                RoleName=str(getenv("ROLE_NAME")),
                AssumeRolePolicyDocument=json.dumps(assumeRolePolicyDocument),
                Description=str(getenv("DESCRIPTION")),
            )
            print(f"IAM Role Created {response['Role']['Arn']}")

            # Store the role's ARN in an environment variable
            environ["AWS_ROLE_ARN"] = response['Role']['Arn']

            response = iam.attach_role_policy(
                RoleName=getenv("ROLE_NAME"),
                PolicyArn=str(getenv("MANAGED_FULLACCESS_EC2_POLICY_ARN"))
            )
            print(f"IAM Role Policy {response} attached to xxx")

        except ClientError as e:
            print(f'\n\nError in IAMRole File\n{e}')
