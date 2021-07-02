import boto3
from os import getenv
from pyaml_env import parse_config
from dotenv import load_dotenv

from app.ec2_instance import EC2Instance
from app.ec2_key_pair import EC2KeyPair
from app.iam_instance_profile import IAMInstanceProfile
from app.iam_role import IAMRole
from app.security_group import SecurityGroup

load_dotenv()


def create_session(session="AYSession"):
    """Set up Boto3 Session

    Args:

    Returns:
        Object: Authenticated Boto3 session.
    """
    AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
    AWS_ROLE_ARN = getenv("AWS_ROLE_ARN")
    AWS_PROFILE = getenv("AWS_PROFILE")
    REGION = getenv("REGION")

    if AWS_ROLE_ARN:
        sts_client = boto3.client("sts", region_name=REGION)
        creds = sts_client.assume_role(RoleArn=AWS_ROLE_ARN,
                                       RoleSessionName=session)
        aws_access_key_id = creds['Credentials']['AccessKeyId']
        aws_secret_access_key = creds['Credentials']['SecretAccessKey']
        aws_session_token = creds['Credentials']['SessionToken']

        session = boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=REGION,
            profile_name=AWS_PROFILE if AWS_PROFILE is not None else None,
        )
    else:
        session = boto3.session.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION,
            profile_name=AWS_PROFILE if AWS_PROFILE is not None else None,
        )

    return session


def main():
    session = create_session()

    keypairs = EC2KeyPair(config=parse_config("./config.yaml")['server'],
                          file_path='/tmp',
                          session=session)
    keypairs.create()
    IAMRole.create(session)
    IAMInstanceProfile.create(session)
    SecurityGroup.create(session)
    ec2 = EC2Instance(keypairs.parse_vars(), session)
    ec2.launch()
    ec2.attach_profile()


if __name__ == "__main__":
    main()
