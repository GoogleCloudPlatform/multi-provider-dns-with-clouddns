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

import google_crc32c
from google.cloud import secretmanager


def list_secrets(project_id):
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"

    list_secrets = []

    for secret in client.list_secrets(request={"parent": parent}):
        secret_name = secret.name.rpartition('/')[2]
        list_secrets.append(secret_name)

    return list_secrets


def access_secret(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    response = client.access_secret_version(request={"name": name})

    crc32c = google_crc32c.Checksum()
    crc32c.update(response.payload.data)
    if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
        print("Data corruption detected.")
        return response

    payload = response.payload.data.decode("UTF-8")
    return payload


def create_secret(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    project_detail = f"projects/{project_id}"
    response = client.create_secret(
        request={
            "parent": project_detail,
            "secret_id": secret_id,
            "secret": {"replication": {"automatic": {}}},
        }
    )
    return response


def create_secret_version(project_id, secret_id, data):
    client = secretmanager.SecretManagerServiceClient()
    parent = client.secret_path(project_id, secret_id)
    response = client.add_secret_version(
        request={"parent": parent,
                 "payload": {"data": data.encode("UTF-8")}}
    )
    return response
