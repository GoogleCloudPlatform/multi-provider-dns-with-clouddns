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

import yaml
import json
import os
from azure.core.exceptions import ResourceNotFoundError, ClientAuthenticationError
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.dns import DnsManagementClient
from azure.identity import ClientSecretCredential


def check_credentials(directory_id, subscription_id, client_id, authentication_key, resource_group):
    try:
        credential = ClientSecretCredential(tenant_id=directory_id, client_id=client_id, client_secret=authentication_key)
        resource_client = ResourceManagementClient(credential, subscription_id)
    except ClientAuthenticationError:
        return False

    try:
        resource_client.resource_groups.get(resource_group)
        return True
    except ResourceNotFoundError:
        return False


def get_zones(directory_id, subscription_id, client_id, authentication_key, resource_group):
    zones = []
    credential = ClientSecretCredential(tenant_id=directory_id, client_id=client_id, client_secret=authentication_key)
    dns_client = DnsManagementClient(credential, subscription_id)
    response = dns_client.zones.list_by_resource_group(resource_group_name=resource_group)

    for item in response:
        zones.append(item.name + '.' + '\n')
    data = ''.join(zones)

    return data


def gen_pipeline():

    if os.environ.get('MACHINE_TYPE'):
        data_plan = {"steps": [{"name": "$_GAR_REGION-docker.pkg.dev/$PROJECT_ID/$_GAR_REPOSITORY/clouddns-haa:latest", "id": "Build OctoDNS Config", "entrypoint": "python3", "args": ["config.py"], "env": ["PROVIDER=${_PROVIDER}", "PROJECT_ID=$PROJECT_ID"], "secretEnv": ["AZURE_DIRECTORY_ID", "AZURE_SUBSCRIPTION_ID", "AZURE_APPLICATION_ID", "AZURE_AUTHENTICATION_KEY", "AZURE_RESOURCE_GROUP"]}, {"name": "$_GAR_REGION-docker.pkg.dev/$PROJECT_ID/$_GAR_REPOSITORY/clouddns-haa:latest", "id": "OctoDNS Sync Plan", "entrypoint": "octodns-sync", "args": ["--config-file=config.yaml"], "secretEnv": ["AZURE_DIRECTORY_ID", "AZURE_SUBSCRIPTION_ID", "AZURE_APPLICATION_ID", "AZURE_AUTHENTICATION_KEY", "AZURE_RESOURCE_GROUP"]}], "options":{"machineType":f"{os.environ.get('MACHINE_TYPE')}"}, "availableSecrets": {"secretManager": [{"versionName": "projects/$PROJECT_ID/secrets/AZURE_DIRECTORY_ID/versions/latest", "env": "AZURE_DIRECTORY_ID"}, {"versionName": "projects/$PROJECT_ID/secrets/AZURE_SUBSCRIPTION_ID/versions/latest", "env": "AZURE_SUBSCRIPTION_ID"}, {"versionName": "projects/$PROJECT_ID/secrets/AZURE_APPLICATION_ID/versions/latest", "env": "AZURE_APPLICATION_ID"}, {"versionName": "projects/$PROJECT_ID/secrets/AZURE_AUTHENTICATION_KEY/versions/latest", "env": "AZURE_AUTHENTICATION_KEY"}, {"versionName": "projects/$PROJECT_ID/secrets/AZURE_RESOURCE_GROUP/versions/latest", "env": "AZURE_RESOURCE_GROUP"}]}}
        data_apply = {"steps": [{"name": "$_GAR_REGION-docker.pkg.dev/$PROJECT_ID/$_GAR_REPOSITORY/clouddns-haa:latest", "id": "Build OctoDNS Config", "entrypoint": "python3", "args": ["config.py"], "env": ["PROVIDER=${_PROVIDER}", "PROJECT_ID=$PROJECT_ID"], "secretEnv": ["AZURE_DIRECTORY_ID", "AZURE_SUBSCRIPTION_ID", "AZURE_APPLICATION_ID", "AZURE_AUTHENTICATION_KEY", "AZURE_RESOURCE_GROUP"]}, {"name": "$_GAR_REGION-docker.pkg.dev/$PROJECT_ID/$_GAR_REPOSITORY/clouddns-haa:latest", "id": "OctoDNS Sync Apply", "entrypoint": "octodns-sync", "args": ["--config-file=config.yaml", "--doit"], "secretEnv": ["AZURE_DIRECTORY_ID", "AZURE_SUBSCRIPTION_ID", "AZURE_APPLICATION_ID", "AZURE_AUTHENTICATION_KEY", "AZURE_RESOURCE_GROUP"]}], "options":{"machineType":f"{os.environ.get('MACHINE_TYPE')}"}, "availableSecrets": {"secretManager": [{"versionName": "projects/$PROJECT_ID/secrets/AZURE_DIRECTORY_ID/versions/latest", "env": "AZURE_DIRECTORY_ID"}, {"versionName": "projects/$PROJECT_ID/secrets/AZURE_SUBSCRIPTION_ID/versions/latest", "env": "AZURE_SUBSCRIPTION_ID"}, {"versionName": "projects/$PROJECT_ID/secrets/AZURE_APPLICATION_ID/versions/latest", "env": "AZURE_APPLICATION_ID"}, {"versionName": "projects/$PROJECT_ID/secrets/AZURE_AUTHENTICATION_KEY/versions/latest", "env": "AZURE_AUTHENTICATION_KEY"}, {"versionName": "projects/$PROJECT_ID/secrets/AZURE_RESOURCE_GROUP/versions/latest", "env": "AZURE_RESOURCE_GROUP"}]}}
    else:
        data_plan = {"steps": [{"name": "$_GAR_REGION-docker.pkg.dev/$PROJECT_ID/$_GAR_REPOSITORY/clouddns-haa:latest", "id": "Build OctoDNS Config", "entrypoint": "python3", "args": ["config.py"], "env": ["PROVIDER=${_PROVIDER}", "PROJECT_ID=$PROJECT_ID"], "secretEnv": ["AZURE_DIRECTORY_ID", "AZURE_SUBSCRIPTION_ID", "AZURE_APPLICATION_ID", "AZURE_AUTHENTICATION_KEY", "AZURE_RESOURCE_GROUP"]}, {"name": "$_GAR_REGION-docker.pkg.dev/$PROJECT_ID/$_GAR_REPOSITORY/clouddns-haa:latest", "id": "OctoDNS Sync Plan", "entrypoint": "octodns-sync", "args": ["--config-file=config.yaml"], "secretEnv": ["AZURE_DIRECTORY_ID", "AZURE_SUBSCRIPTION_ID", "AZURE_APPLICATION_ID", "AZURE_AUTHENTICATION_KEY", "AZURE_RESOURCE_GROUP"]}], "availableSecrets": {"secretManager": [{"versionName": "projects/$PROJECT_ID/secrets/AZURE_DIRECTORY_ID/versions/latest", "env": "AZURE_DIRECTORY_ID"}, {"versionName": "projects/$PROJECT_ID/secrets/AZURE_SUBSCRIPTION_ID/versions/latest", "env": "AZURE_SUBSCRIPTION_ID"}, {"versionName": "projects/$PROJECT_ID/secrets/AZURE_APPLICATION_ID/versions/latest", "env": "AZURE_APPLICATION_ID"}, {"versionName": "projects/$PROJECT_ID/secrets/AZURE_AUTHENTICATION_KEY/versions/latest", "env": "AZURE_AUTHENTICATION_KEY"}, {"versionName": "projects/$PROJECT_ID/secrets/AZURE_RESOURCE_GROUP/versions/latest", "env": "AZURE_RESOURCE_GROUP"}]}}
        data_apply = {"steps": [{"name": "$_GAR_REGION-docker.pkg.dev/$PROJECT_ID/$_GAR_REPOSITORY/clouddns-haa:latest", "id": "Build OctoDNS Config", "entrypoint": "python3", "args": ["config.py"], "env": ["PROVIDER=${_PROVIDER}", "PROJECT_ID=$PROJECT_ID"], "secretEnv": ["AZURE_DIRECTORY_ID", "AZURE_SUBSCRIPTION_ID", "AZURE_APPLICATION_ID", "AZURE_AUTHENTICATION_KEY", "AZURE_RESOURCE_GROUP"]}, {"name": "$_GAR_REGION-docker.pkg.dev/$PROJECT_ID/$_GAR_REPOSITORY/clouddns-haa:latest", "id": "OctoDNS Sync Apply", "entrypoint": "octodns-sync", "args": ["--config-file=config.yaml", "--doit"], "secretEnv": ["AZURE_DIRECTORY_ID", "AZURE_SUBSCRIPTION_ID", "AZURE_APPLICATION_ID", "AZURE_AUTHENTICATION_KEY", "AZURE_RESOURCE_GROUP"]}], "availableSecrets": {"secretManager": [{"versionName": "projects/$PROJECT_ID/secrets/AZURE_DIRECTORY_ID/versions/latest", "env": "AZURE_DIRECTORY_ID"}, {"versionName": "projects/$PROJECT_ID/secrets/AZURE_SUBSCRIPTION_ID/versions/latest", "env": "AZURE_SUBSCRIPTION_ID"}, {"versionName": "projects/$PROJECT_ID/secrets/AZURE_APPLICATION_ID/versions/latest", "env": "AZURE_APPLICATION_ID"}, {"versionName": "projects/$PROJECT_ID/secrets/AZURE_AUTHENTICATION_KEY/versions/latest", "env": "AZURE_AUTHENTICATION_KEY"}, {"versionName": "projects/$PROJECT_ID/secrets/AZURE_RESOURCE_GROUP/versions/latest", "env": "AZURE_RESOURCE_GROUP"}]}}

    file_plan = open('clouddns-haa-plan.json', 'w+')
    file_apply = open('clouddns-haa-apply.json', 'w+')
    # yaml.dump(data, f, default_flow_style=True, sort_keys=False)
    json.dump(data_plan, file_plan, indent=2)
    json.dump(data_apply, file_apply, indent=2)


def gen_config(project_id, zones):
    cfg = {'providers': {}}
    cfg['providers']['azure'] = {
        'class': 'octodns_azure.AzureProvider',
        'client_id': 'env/AZURE_APPLICATION_ID',
        'key': 'env/AZURE_AUTHENTICATION_KEY',
        'directory_id': 'env/AZURE_DIRECTORY_ID',
        'sub_id': 'env/AZURE_SUBSCRIPTION_ID',
        'resource_group': 'env/AZURE_RESOURCE_GROUP'}
    cfg['providers']['google_cloud'] = {
        'class': 'octodns_googlecloud.GoogleCloudProvider',
        'project': f'{project_id}'}
    cfg['zones'] = {}
    for zone in zones.splitlines():
        cfg['zones'][f'{zone}'] = {
            'sources': ['azure'],
            'targets': ['google_cloud']
        }

    f = open('config.yaml', 'w+')
    yaml.dump(cfg, f)
