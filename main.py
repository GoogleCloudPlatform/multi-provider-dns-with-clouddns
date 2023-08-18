#  Copyright 2023 Google Inc. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import getpass
import argparse
import gcp

def create_secret(project_id, secret_ids):
    for secret in secret_ids:
        try:
            gcp.create_secret(project_id, secret)
        except Exception as e:
            print(e)
            continue
        gcp.create_secret_version(project_id, secret, secret_ids[secret])
        print(f'{secret} secret created in Secret Manager.')

if __name__ == "__main__":
    crd_secret = argparse.ArgumentParser(prog='crd_secret',
                                        description='Use this code to create the credential secret.',
                                        usage='%(prog)s provider',
                                        allow_abbrev=False)
    crd_secret.add_argument('Provider', metavar='provider', type=str.lower,
                            choices=['route53', 'azure'], help='name of your source dns provider.')

    args = crd_secret.parse_args()
    input_provider = args.Provider

    project_id = os.environ.get('CDNS_PROJECT_ID')

    print(f'Current Project: {project_id}')

    secret_ids = {}

    if input_provider == 'route53':
        import aws as src_dns
        if os.environ.get('AWS_ACCESS_KEY_ID') and os.environ.get('AWS_SECRET_ACCESS_KEY'):
            aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
            aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        else:
            aws_access_key_id = getpass.getpass('AWS_ACCESS_KEY_ID: ')
            aws_secret_access_key = getpass.getpass('AWS_SECRET_ACCESS_KEY: ')

        if src_dns.check_credential(aws_access_key_id, aws_secret_access_key):
            print('Credentials Validated...')
            print('Saving Credentials in GCP Secret Manager...')
            secret_ids = {'AWS_ACCESS_KEY_ID': aws_access_key_id,
                        'AWS_SECRET_ACCESS_KEY': aws_secret_access_key}

    elif input_provider == 'azure':
        import az as src_dns
        if os.environ.get('AZURE_DIRECTORY_ID') and os.environ.get('AZURE_SUBSCRIPTION_ID') and os.environ.get('AZURE_APPLICATION_ID') and os.environ.get('AZURE_AUTHENTICATION_KEY') and os.environ.get('AZURE_RESOURCE_GROUP'):
            directory_id = os.environ.get('AZURE_DIRECTORY_ID')
            subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID')
            client_id = os.environ.get('AZURE_APPLICATION_ID')
            authentication_key = os.environ.get('AZURE_AUTHENTICATION_KEY')
            resource_group = os.environ.get('AZURE_RESOURCE_GROUP')
        else:
            directory_id = getpass.getpass('AZURE_DIRECTORY_ID: ')
            subscription_id = getpass.getpass('AZURE_SUBSCRIPTION_ID: ')
            client_id = getpass.getpass('AZURE_APPLICATION_ID: ')
            authentication_key = getpass.getpass('AZURE_AUTHENTICATION_KEY: ')
            resource_group = getpass.getpass('AZURE_RESOURCE_GROUP: ')

        if src_dns.check_credentials(directory_id, subscription_id, client_id, authentication_key, resource_group):
            print('Credentials Validated...')
            print('Saving Credentials in GCP Secret Manager...')
            secret_ids = {'AZURE_DIRECTORY_ID': directory_id,
                        'AZURE_SUBSCRIPTION_ID': subscription_id,
                        'AZURE_APPLICATION_ID': client_id,
                        'AZURE_AUTHENTICATION_KEY': authentication_key,
                        'AZURE_RESOURCE_GROUP': resource_group}

    create_secret(project_id, secret_ids)

    src_dns.gen_pipeline()
