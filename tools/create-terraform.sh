#!/bin/bash

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

echo "------
Create project and link billing account 
------"
gcloud projects create $TF_PROJECT_ID --folder=$FOLDER_ID --set-as-default
gcloud beta billing projects link $TF_PROJECT_ID --billing-account $BILLING_ACCOUNT
echo "------
Enable needed APIs 
------"
gcloud services enable cloudbilling.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable iam.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
echo "------
Create Bucket 
----"
gcloud storage buckets create gs://$TF_BUCKET_NAME --project=$TF_PROJECT_ID --uniform-bucket-level-access --public-access-prevention --location=$REGION

echo Create Terraform Service Account ------
gcloud iam service-accounts create $TF_SA_NAME \
    --description="Terraform Service Account" \
    --display-name=$TF_SA_NAME \
    --project=$TF_PROJECT_ID
echo "------
Grant Access
Grant Storage Object Admin Role to Service Account 
------"
gsutil iam ch serviceAccount:$TF_SA_NAME@$TF_PROJECT_ID.iam.gserviceaccount.com:roles/storage.objectAdmin gs://$TF_BUCKET_NAME

echo "------
Grant Service Account Access to the Organization to create project, assign billing, and manage IAM policiy
------"
gcloud resource-manager folders add-iam-policy-binding $FOLDER_ID \
--member=serviceAccount:$TF_SA_NAME@$TF_PROJECT_ID.iam.gserviceaccount.com \
--role=roles/resourcemanager.projectCreator

gcloud resource-manager folders add-iam-policy-binding $FOLDER_ID \
--member=serviceAccount:$TF_SA_NAME@$TF_PROJECT_ID.iam.gserviceaccount.com \
--role=roles/resourcemanager.projectDeleter

gcloud resource-manager folders add-iam-policy-binding $FOLDER_ID \
--member=serviceAccount:$TF_SA_NAME@$TF_PROJECT_ID.iam.gserviceaccount.com \
--role=roles/resourcemanager.projectIamAdmin

gcloud resource-manager folders add-iam-policy-binding $FOLDER_ID \
--member=serviceAccount:$TF_SA_NAME@$TF_PROJECT_ID.iam.gserviceaccount.com \
--role=roles/iam.serviceAccountAdmin

if [[ -z "${BILLING_ORG_ID}" ]]; then
  gcloud organizations add-iam-policy-binding $ORGANIZATION_ID \
    --member=serviceAccount:$TF_SA_NAME@$TF_PROJECT_ID.iam.gserviceaccount.com --role=roles/billing.user
else
  gcloud organizations add-iam-policy-binding $BILLING_ORG_ID \
    --member=serviceAccount:$TF_SA_NAME@$TF_PROJECT_ID.iam.gserviceaccount.com --role=roles/billing.user
fi

echo "------
Grant User Access to the Service Account
------"
gcloud iam service-accounts add-iam-policy-binding \
    $TF_SA_NAME@$TF_PROJECT_ID.iam.gserviceaccount.com \
    --member="user:$USER_ACCOUNT" \
    --role="roles/iam.serviceAccountUser"

gcloud iam service-accounts add-iam-policy-binding \
    $TF_SA_NAME@$TF_PROJECT_ID.iam.gserviceaccount.com \
    --member="user:$USER_ACCOUNT" \
    --role="roles/iam.serviceAccountTokenCreator"

echo "------
Waiting roles to propagate, 10 sec"
sleep 10s
echo "------ DONE ------"
