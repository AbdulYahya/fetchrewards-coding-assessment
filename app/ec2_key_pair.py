from botocore.exceptions import ClientError
from shlex import quote
from subprocess import run, PIPE
from os import (getenv,
                environ,
                open,
                fdopen,
                O_WRONLY,
                O_CREAT,
                path,
                R_OK,
                access)

from pyaml_env import parse_config


class EC2KeyPair:
    def __init__(self,
                 config,
                 file_path,
                 session):
        self.config = config
        self.file_path = file_path
        self.session = session
        self.ec2 = self.session.client('ec2', getenv('REGION'))

    def create(self):
        try:
            # Generate EC2 Instance KeyPair
            self.generate_keys(f"{self.file_path}/root_key.pem", 'root_key')
            users = self.config['users']

            for user in users:
                key_name = f"{user['login'].upper()}_SSH_PUBLIC_KEY"
                file_path = f"{self.file_path}/{key_name}.pem"

                if path.isfile(file_path) and access(file_path,
                                                     R_OK):
                    del_temp_ssh_file_cmd = 'rm -rf {}'.format(
                        quote(file_path))
                    run([del_temp_ssh_file_cmd],
                        shell=True,
                        stdout=PIPE,
                        text=True,
                        check=True)

                    self.generate_keys(file_path, key_name.upper())
                else:
                    self.generate_keys(file_path, key_name.upper())

                # Retrieve & Store Public Key as environment variable
                shell_cmd = 'ssh-keygen -y -f {}'.format(quote(file_path))
                public_key = run([shell_cmd], shell=True,
                                 stdout=PIPE, text=True, check=True)

                environ[key_name] = public_key.stdout

            self.config = parse_config("./config.yaml")

        except ClientError as e:
            print(f'\n\nError in Key Pairs File\n{e}')

    def generate_keys(self, file_path, key_name):
        key_pair = self.ec2.create_key_pair(KeyName=key_name)
        private_key = key_pair["KeyMaterial"]

        with fdopen(open(file_path,
                    O_WRONLY | O_CREAT,
                    0o400), "w+") as handle:
            # Write Private Key
            handle.write(private_key)
            # environ[f"{key_name}_SSH_KEY"]
            print(f"Created {key_name} SSH KeyPair!")

    def parse_vars(self):
        return self.config
