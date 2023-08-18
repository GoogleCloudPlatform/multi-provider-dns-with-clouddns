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
import boto3
import botocore


def check_credential(aws_access_key, aws_secret_key):
    sts = boto3.client('sts', aws_access_key_id=aws_access_key,
                       aws_secret_access_key=aws_secret_key)
    try:
        sts.get_caller_identity()
        return True
    except botocore.exceptions.ClientError:
        print("Invalid Credentials")
        return False


def get_zones(aws_access_key, aws_secret_key):
    client = boto3.client('route53',
                          aws_access_key_id=aws_access_key,
                          aws_secret_access_key=aws_secret_key)

    zones = []
    count_zones = 0

    pages = True
    next_page = {}

    while pages:
        response = client.list_hosted_zones(**next_page)
        for zone in response['HostedZones']:
            count_zones += 1
            zones.append(zone['Name']+'\n')
        data = ''.join(zones)
        pages = response['IsTruncated']
        next_page['Marker'] = response.get('NextMarker', None)
        print(f"Found {count_zones} zones...")
    return data


def gen_pipeline():

    if os.environ.get('MACHINE_TYPE'):
        data_plan = {"steps": [{"name": "$_GAR_REGION-docker.pkg.dev/$PROJECT_ID/$_GAR_REPOSITORY/clouddns-haa:latest", "id": "Build OctoDNS Config", "entrypoint": "python3", "args": ["config.py"], "env": ["PROVIDER=${_PROVIDER}", "PROJECT_ID=$PROJECT_ID"], "secretEnv": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]}, {"name": "$_GAR_REGION-docker.pkg.dev/$PROJECT_ID/$_GAR_REPOSITORY/clouddns-haa:latest", "id": "OctoDNS Sync Plan", "entrypoint": "octodns-sync",
                                                                                                                                                                                                                                                                                                                                 "args": ["--config-file=config.yaml"], "secretEnv": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]}], "options": {"machineType": f"{os.environ.get('MACHINE_TYPE')}"}, "availableSecrets": {"secretManager": [{"versionName": "projects/$PROJECT_ID/secrets/AWS_ACCESS_KEY_ID/versions/latest", "env": "AWS_ACCESS_KEY_ID"}, {"versionName": "projects/$PROJECT_ID/secrets/AWS_SECRET_ACCESS_KEY/versions/latest", "env": "AWS_SECRET_ACCESS_KEY"}]}}
        data_apply = {"steps": [{"name": "$_GAR_REGION-docker.pkg.dev/$PROJECT_ID/$_GAR_REPOSITORY/clouddns-haa:latest", "id": "Build OctoDNS Config", "entrypoint": "python3", "args": ["config.py"], "env": ["PROVIDER=${_PROVIDER}", "PROJECT_ID=$PROJECT_ID"], "secretEnv": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]}, {"name": "$_GAR_REGION-docker.pkg.dev/$PROJECT_ID/$_GAR_REPOSITORY/clouddns-haa:latest", "id": "OctoDNS Sync Apply", "entrypoint": "octodns-sync",
                                                                                                                                                                                                                                                                                                                                  "args": ["--config-file=config.yaml", "--doit"], "secretEnv": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]}], "options": {"machineType": f"{os.environ.get('MACHINE_TYPE')}"}, "availableSecrets": {"secretManager": [{"versionName": "projects/$PROJECT_ID/secrets/AWS_ACCESS_KEY_ID/versions/latest", "env": "AWS_ACCESS_KEY_ID"}, {"versionName": "projects/$PROJECT_ID/secrets/AWS_SECRET_ACCESS_KEY/versions/latest", "env": "AWS_SECRET_ACCESS_KEY"}]}}
    else:
        data_plan = {"steps": [{"name": "$_GAR_REGION-docker.pkg.dev/$PROJECT_ID/$_GAR_REPOSITORY/clouddns-haa:latest", "id": "Build OctoDNS Config", "entrypoint": "python3", "args": ["config.py"], "env": ["PROVIDER=${_PROVIDER}", "PROJECT_ID=$PROJECT_ID"], "secretEnv": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]}, {"name": "$_GAR_REGION-docker.pkg.dev/$PROJECT_ID/$_GAR_REPOSITORY/clouddns-haa:latest", "id": "OctoDNS Sync Plan",
                                                                                                                                                                                                                                                                                                                                 "entrypoint": "octodns-sync", "args": ["--config-file=config.yaml"], "secretEnv": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]}], "availableSecrets": {"secretManager": [{"versionName": "projects/$PROJECT_ID/secrets/AWS_ACCESS_KEY_ID/versions/latest", "env": "AWS_ACCESS_KEY_ID"}, {"versionName": "projects/$PROJECT_ID/secrets/AWS_SECRET_ACCESS_KEY/versions/latest", "env": "AWS_SECRET_ACCESS_KEY"}]}}
        data_apply = {"steps": [{"name": "$_GAR_REGION-docker.pkg.dev/$PROJECT_ID/$_GAR_REPOSITORY/clouddns-haa:latest", "id": "Build OctoDNS Config", "entrypoint": "python3", "args": ["config.py"], "env": ["PROVIDER=${_PROVIDER}", "PROJECT_ID=$PROJECT_ID"], "secretEnv": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]}, {"name": "$_GAR_REGION-docker.pkg.dev/$PROJECT_ID/$_GAR_REPOSITORY/clouddns-haa:latest", "id": "OctoDNS Sync Apply",
                                                                                                                                                                                                                                                                                                                                  "entrypoint": "octodns-sync", "args": ["--config-file=config.yaml", "--doit"], "secretEnv": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]}], "availableSecrets": {"secretManager": [{"versionName": "projects/$PROJECT_ID/secrets/AWS_ACCESS_KEY_ID/versions/latest", "env": "AWS_ACCESS_KEY_ID"}, {"versionName": "projects/$PROJECT_ID/secrets/AWS_SECRET_ACCESS_KEY/versions/latest", "env": "AWS_SECRET_ACCESS_KEY"}]}}

    file_plan = open('clouddns-haa-plan.json', 'w+')
    file_apply = open('clouddns-haa-apply.json', 'w+')

    json.dump(data_plan, file_plan, indent=2)
    json.dump(data_apply, file_apply, indent=2)


def gen_config(project_id, zones):
    cfg = {'providers': {}}
    cfg['providers'] = {}
    cfg['providers']['route53'] = {
        'class': 'octodns_route53.Route53Provider',
        'access_key_id': 'env/AWS_ACCESS_KEY_ID',
        'secret_access_key': 'env/AWS_SECRET_ACCESS_KEY',
        'client_max_attempts': 10}
    cfg['providers']['google_cloud'] = {
        'class': 'octodns_googlecloud.GoogleCloudProvider',
        'project': f'{project_id}'}
    cfg['zones'] = {}
    for zone in zones.splitlines():
        cfg['zones'][f'{zone}'] = {
            'sources': ['route53'],
            'targets': ['google_cloud']
        }

    f = open('config.yaml', 'w+')
    yaml.dump(cfg, f)
