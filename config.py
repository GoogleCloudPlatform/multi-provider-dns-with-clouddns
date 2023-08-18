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
import gcp

project_id = os.environ.get('PROJECT_ID')
provider = os.environ.get('PROVIDER')

if provider == 'route53':
    import aws as src_dns
elif provider == 'azure':
    import az as src_dns

print('project_id: ',project_id)
print('provider: ',provider)

if f"{provider.upper()}_ZONES" in gcp.list_secrets(project_id):
    data = gcp.access_secret(project_id, f"{provider.upper()}_ZONES")
else:
    if provider == 'route53':
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

        data = src_dns.get_zones(aws_access_key_id, aws_secret_access_key)
            
    elif provider == 'azure':
        directory_id = os.environ.get('AZURE_DIRECTORY_ID')
        subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID')
        client_id = os.environ.get('AZURE_APPLICATION_ID')
        authentication_key = os.environ.get('AZURE_AUTHENTICATION_KEY')
        resource_group = os.environ.get('AZURE_RESOURCE_GROUP')

        data = src_dns.get_zones(directory_id, subscription_id, client_id, authentication_key, resource_group)

print('Generating OctoDNS config.yaml file...')
src_dns.gen_config(project_id, data)
