# High Available DNS leveraging a Multi Cloud Implementation

This guide intends to help you use this repository to set up your environment with all required resources, including [OctoDNS](https://github.com/octodns/octodns) to sync your current provider with Google Cloud DNS.

**ATTENTION**: Make sure you have all prerequisites detailed in the [README](README.md) file.

## What we will be doing

1. Grant Initial Permissions
1. Gather Requirements
1. Configure Terraform environment
1. Gather source provider credentials
1. Deploy Infrastructure  using Terraform 
1. Configure the solution 
1. Execute the synchronization Pipelines
1. Check Result on Cloud DNS

## General Requirements

1. The user account deploying this solution will need to have some permissions (detailed in the next step)
1. Credentials with permissions to access the source provider

## Grant Initial Permissions

To be able to run all steps and deploy the solution, go to the GCP Console and make sure that the user account have the following permissions in:

- Organization Level
    - **Billing Account User**: Required to be able to link the billing account to new projects (terraform bootstrap)
    - **Organization Administrator**: Required to grant billing account permissions to Terraform Service Account
      
- Folder Level
    - **Project Creator**: Required to be able to create new projects (terraform bootstrap).
    - **Project Deleter (Optional)**: Required to be able to delete projects at the end to clean up.
    - **Folder IAM Admin**: Required to grant permissions to terraform service account.
    - **Project IAM Admin**: Required to grant permissions to terraform service account.

## Gather Source Provider Credentials

We will need the access secrets for the source provider (Service Accounts/Principals), please check below the necessary Keys and permission for each provider

Route 53:
- Policy:
  - **[AmazonRoute53ReadOnlyAccess](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonRoute53ReadOnlyAccess.html)**: provides read only access to all Amazon Route 53
- Credentials:
  - AWS_ACCESS_KEY_ID 
  - AWS_SECRET_ACCESS_KEY

    __Note:__: You may follow this [reference](https://docs.aws.amazon.com/cli/latest/reference/iam/create-access-key.html) for creating and gathering the access key information.


Azure:
- Role:
  - **[DNS Zone Contributor](https://learn.microsoft.com/en-us/azure/dns/dns-protect-zones-recordsets)**: built-in role for managing private DNS resources
- Credentials:
  - AZURE_AUTHENTICATION_KEY | password or auth token
  - AZURE_APPLICATION_ID     | service principal id
  - AZURE_DIRECTORY_ID       | tenant or parent management group
  - AZURE_SUBSCRIPTION_ID
  - AZURE_RESOURCE_GROUP

    __Note:__ Yoy may follow this [reference](https://learn.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli) for creating and gathering the service principal information.

## Prepare the Environment

We are going to configure environment variables to fill required values for the whole process.

### Define Environment Variables

Replace the following values with the specific values for your project in the .env file. 

Please note that there is an .env.example file. Replace the values, rename it to .env, then proceed to the import command below.

### Enable Trigger Webhook (Active/Passive Set Up)

Recommended to use in a Active/Active set up, where you would be able to integrate your current pipeline with this solution by invoking the **Webhook**.

More details in the **Next Steps** section of this guide.

### Enable Trigger Scheduler (Active/Active Set Up)

For an Active/Passive set up, where you mostly will use as a fallback in case of disaster of your current provider, scheduling a periodic synchronization would be enough to keep both providers in sync.

To Enable scheduler, you have just to set the variable `SCHEDULE=True`, define `SCHEDULER_TIME_ZONE="<Timezone>"` and the trigger interval `SCHEDULER_CRON="*/5 * * * *"`, in this case, every 5 minutes. 

More details in the **Next Steps** section of this guide.

### Enable Trigger Approval

You can choose `true` or `false` for the **approval** variable (`TRIGGER_PLAN_APPROVAL` or `TRIGGER_APPLY_APPROVAL`) for the **triggers**, for each value please note:

- **True** values means that you will have to go to the **Dashboard Console** of **Cloud Build** and manually approve the trigger after clicking on **Run trigger** (**Not recommended for when using webhooks or scheduler**)

- **False** values means that there'll be no need for approval and it will be automatic. 

**INFO**: For a better understanding about each of the variables mentioned in this section, please consult the terraform/README [here](terraform/README.md).

**NOTE**: With everything ready, the first synchronization will take more time to run than the subsequent runs. By our tests it may vary between 1 to 5 records per second. Two basic tests:

    a. 250 zones with 25 records each took 31 minutes; 
    b. 1000 zones with 25 records took 4.15 Hours. After the first sync, without any change every sync will last no more than 5 minutes, in our tests, with 5000 zones it took 3 min/avg.s

```sh
cp .env.example .env
nano .env
```

**Tips**: If you are using Cloud Shell Tutorials, you can open the example file by clicking <walkthrough-editor-open-file filePath=".env.example">here</walkthrough-editor-open-file>, save as and do your changes

After the values were replaced, import the variables using:

```sh 
set -o allexport
source .env
set +o allexport
```


**Example Variables**

Please check below the variables used in the project. Note that these are the same vars located inside the .env.example file to be replaced and exported.

```
# basic required values
USER_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")
ORGANIZATION_ID=<org id numeric>
BILLING_ACCOUNT=<billing id>
FOLDER_ID=<parent folder id for the bootstrap and clouddns project>
REGION=<default region for resources>
ZONE=<default zone for resources>
TF_PROJECT_ID=<CHANGE-ME>-clouddns-sync-bs-0000 <project id for the bootstrap project>
TF_SA_NAME=sa-clouddns-tf
TF_BUCKET_NAME=$TF_PROJECT_ID-bucket-tfstate
SOURCE_PROVIDER=<route53 or azure>

# (optional features, uncomment to use)

# if the billing to be used is linked to another organization.
# BILLING_ORG_ID=<billing org id if its a different> 

# if you need a better performance in Cloud Build, this variable let you set the machine type you wish.
# MACHINE_TYPE=<UNSPECIFIED or N1_HIGHCPU_8 or N1_HIGHCPU_32 or E2_HIGHCPU_8 or E2_HIGHCPU_32>

# false by default, change this to true to enable webhook execution trigger.
TRIGGER_WEBHOOK=false
# TRIGGER_PLAN_APPROVAL=<true or false>
# TRIGGER_APPLY_APPROVAL=<true or false>

# false by default, change this to true to enable scheduled execution of the apply trigger.
# if changing to true, set SCHEDULER_TIME_ZONE and SCHEDULER_CRON appropriately.
# It is only available if the triggers are not event webhook.
SCHEDULER=false
# SCHEDULER_TIME_ZONE="America/New_York" # or according your location
# SCHEDULER_CRON="*/8 * * * *" # according your strategy - this example, every 8 minutes

# if you want to use an existing project where you want to deploy the solution, these variables let you define it.
# EXISTING_PROJECT_ID=<existing project id>
# EXISTING_PROJECT_NUMBER=<existing project number>
# EXISTING_SERVICE_ACCOUNT=<existing service account>
# EXISTING_SERVICE_ACCOUNT_PROJECT_ID=<existing project id where the service account used to deploy the solution resides>

# Used by terraform. Will get from prior variables, usually no need to change. Change only in special use cases.
TF_VAR_user_account=$USER_ACCOUNT
TF_VAR_organization_id=$ORGANIZATION_ID
TF_VAR_billing_account=$BILLING_ACCOUNT
TF_VAR_folder_id=$FOLDER_ID
TF_VAR_region=$REGION
TF_VAR_zone=$ZONE
TF_VAR_source_provider=$SOURCE_PROVIDER
TF_VAR_service_account=$TF_SA_NAME@$TF_PROJECT_ID.iam.gserviceaccount.com
TF_VAR_trigger_webhook=$TRIGGER_WEBHOOK
TF_VAR_plan_approval=$TRIGGER_PLAN_APPROVAL
TF_VAR_apply_approval=$TRIGGER_APPLY_APPROVAL
TF_VAR_scheduler=$SCHEDULER
TF_VAR_scheduler_time_zone=$SCHEDULER_TIME_ZONE
TF_VAR_scheduler_cron=$SCHEDULER_CRON
TF_VAR_existing_project_id=$EXISTING_PROJECT_ID
TF_VAR_existing_project_number=$EXISTING_PROJECT_NUMBER
TF_VAR_existing_service_account=$EXISTING_SERVICE_ACCOUNT

# Source Providers Secrets, if set, will be used by main.py to generate secrets for the pipelines
# AWS
# export AWS_ACCESS_KEY_ID=$(gcloud secrets versions access latest --secret=AWS_ACCESS_KEY_ID --project=<project_id>)
# export AWS_SECRET_ACCESS_KEY=$(gcloud secrets versions access latest --secret=AWS_SECRET_ACCESS_KEY --project=<project_id>)

# Azure
# export AZURE_APPLICATION_ID=$(gcloud secrets versions access latest --secret=AZURE_APPLICATION_ID --project=<project_id>)
# export AZURE_AUTHENTICATION_KEY=$(gcloud secrets versions access latest --secret=AZURE_AUTHENTICATION_KEY --project=<project_id>)
# export AZURE_DIRECTORY_ID=$(gcloud secrets versions access latest --secret=AZURE_DIRECTORY_ID --project=<project_id>)
# export AZURE_SUBSCRIPTION_ID=$(gcloud secrets versions access latest --secret=AZURE_SUBSCRIPTION_ID --project=<project_id>)
# export AZURE_RESOURCE_GROUP=$(gcloud secrets versions access latest --secret=AZURE_RESOURCE_GROUP --project=<project_id>)
```

## Create Terraform project

In this section it's being created the terraform project, once completed there will be:
- A terraform service account with required permissions to create the infrastructure
- User permissions on the terraform service account 
- A bucket to store the state

### Steps via shell script

In order to facilitate the creation of the terraform project, it is provided in this repository an option to implement the commands via a shell script.

Make sure that the environment variables were correctly inserted before running the script. The file is located under the tools folder and can be used as follows:

**ATTENTION**: Make sure you are in the root level of this repository.

```sh
bash tools/create-terraform.sh
```

When running it will do all the commands described in the manual steps, following what was inserted into the environment variables. 

**ATTENTION: Once it's done**, jump to the **Create Infrastructure** section of this Guide and continue the commands to initialize, plan, and apply terraform. 

<walkthrough-footnote>For manual step, continue to **Next** session</walkthrough-footnote>

## Manual Steps

Create the terraform project and link a billing account

```sh
gcloud projects create $TF_PROJECT_ID --folder=$FOLDER_ID --set-as-default
gcloud beta billing projects link $TF_PROJECT_ID --billing-account $BILLING_ACCOUNT
```

### Enable required APIs

Now we need to enable the required APIs to be able to create all the resources

```sh
gcloud services enable cloudbilling.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable iam.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

## Create Bucket to store TF state

Now we are going to create a cloud storage bucket to store the terraform state

```sh
gcloud storage buckets create gs://$TF_BUCKET_NAME --project=$TF_PROJECT_ID --uniform-bucket-level-access --public-access-prevention --location=$REGION
```

## Create the Terraform Service Account

This service account will be used by terraform to create all resources

```sh
gcloud iam service-accounts create $TF_SA_NAME \
    --description="Terraform Service Account" \
    --display-name=$TF_SA_NAME \
    --project=$TF_PROJECT_ID
```

Now, grant Storage Object Admin Role to Terraform Service Account 

```sh
gsutil iam ch serviceAccount:$TF_SA_NAME@$TF_PROJECT_ID.iam.gserviceaccount.com:roles/storage.objectAdmin gs://$TF_BUCKET_NAME
```

## Grant Service Account Rights 

Add the following roles to the terraform service account: 
- Folder Level
    - Project Creator
    - Project Deleter
    - Service Account Admin
    - Project IAM Admin
- Organization Level
    - Billing User

```sh
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
```

## Grant Billing User Rights to the TF Service Account

Add the following to the organization where it's configured the billing, for the service account, as a billing user. 
Execute one of the following commands depending on the billing account:

If the billing belongs to the same organization:
```sh
gcloud organizations add-iam-policy-binding $ORGANIZATION_ID \
    --member=serviceAccount:$TF_SA_NAME@$TF_PROJECT_ID.iam.gserviceaccount.com --role=roles/billing.user
```

`OR` if the billing to be used is linked to another organization:
```sh
gcloud organizations add-iam-policy-binding $BILLING_ORG_ID \
    --member=serviceAccount:$TF_SA_NAME@$TF_PROJECT_ID.iam.gserviceaccount.com --role=roles/billing.user
```

## Grant User Rights to the Service Account

The user that will be using the SA to implement resources, needs to have:
- Service Account User
- Service Account Token Creator 

```sh
gcloud iam service-accounts add-iam-policy-binding \
    $TF_SA_NAME@$TF_PROJECT_ID.iam.gserviceaccount.com \
    --member="user:$USER_ACCOUNT" \
    --role="roles/iam.serviceAccountUser"

gcloud iam service-accounts add-iam-policy-binding \
    $TF_SA_NAME@$TF_PROJECT_ID.iam.gserviceaccount.com \
    --member="user:$USER_ACCOUNT" \
    --role="roles/iam.serviceAccountTokenCreator"
```

**ATTENTION: Once it's done**, jump to the **Create Infrastructure** section of this Guide and continue the commands to initialize, plan, and apply terraform. 

<walkthrough-footnote>For using an existing project, continue to **Next** session</walkthrough-footnote>

## Using an existing project

It is assumed that you already have a project and a sevice account to be [impersonated](https://cloud.google.com/iam/docs/impersonating-service-accounts) by the user who is using the terraform.

**Tips**: You may follow how to create or use a service account created in one of the **Create Terraform project** or **Manual Steps** steps contained in this guide. 

**ATTENTION: For these steps we are going to use EXISTING_PROJECT_ID, EXISTING_PROJECT_NUMBER and EXISTING_SERVICE_ACCOUNT environment vars you have set on `.env`**

### Enable required APIs

Make sure to enable the required APIs on both projects: `existing project` where you will deploy the solution and `existing service account project` where the service account used to deploy the resource resides.

```sh
gcloud services enable cloudbilling.googleapis.com --project=$EXISTING_PROJECT_ID
gcloud services enable cloudbuild.googleapis.com --project=$EXISTING_PROJECT_ID
gcloud services enable sourcerepo.googleapis.com --project=$EXISTING_PROJECT_ID
gcloud services enable artifactregistry.googleapis.com --project=$EXISTING_PROJECT_ID
gcloud services enable secretmanager.googleapis.com --project=$EXISTING_PROJECT_ID
gcloud services enable cloudscheduler.googleapis.com --project=$EXISTING_PROJECT_ID
gcloud services enable dns.googleapis.com --project=$EXISTING_PROJECT_ID
gcloud services enable iam.googleapis.com --project=$EXISTING_PROJECT_ID
gcloud services enable cloudresourcemanager.googleapis.com --project=$EXISTING_PROJECT_ID

gcloud services enable cloudbilling.googleapis.com --project=$EXISTING_SERVICE_ACCOUNT_PROJECT_ID
gcloud services enable cloudbuild.googleapis.com --project=$EXISTING_SERVICE_ACCOUNT_PROJECT_ID
gcloud services enable sourcerepo.googleapis.com --project=$EXISTING_SERVICE_ACCOUNT_PROJECT_ID
gcloud services enable artifactregistry.googleapis.com --project=$EXISTING_SERVICE_ACCOUNT_PROJECT_ID
gcloud services enable secretmanager.googleapis.com --project=$EXISTING_SERVICE_ACCOUNT_PROJECT_ID
gcloud services enable cloudscheduler.googleapis.com --project=$EXISTING_SERVICE_ACCOUNT_PROJECT_ID
gcloud services enable dns.googleapis.com --project=$EXISTING_SERVICE_ACCOUNT_PROJECT_ID
gcloud services enable iam.googleapis.com --project=$EXISTING_SERVICE_ACCOUNT_PROJECT_ID
gcloud services enable cloudresourcemanager.googleapis.com --project=$EXISTING_SERVICE_ACCOUNT_PROJECT_ID
```

__Note:__ Wait few minutes for the actions to propagate. 

### Grant Service Account Rights 

Add the following roles to the terraform service account at project level:

- Artifact Registry Administrator: Required to be able to create the artifact registry repo.
- Secret Manager Admin: Required to be able to create the secret for webhook.
- Source Repository Administrator: Required to be able to create the cloud source repository repo.
- Cloud Build Editor: Required to be able to create the cloud build/triggers.
- Cloud Scheduler Admin: Required to be able to create the cloud scheduler. 
- Service Account User : Required to be able to create the cloud scheduler job by the impersonated S.A
- Project IAM Admin: Required to be able to apply IAM roles in necessary principals to execute the solution
- Service Account Admin: Required to be able to create cloud scheduler service account to create jobs.

```sh
gcloud projects add-iam-policy-binding $EXISTING_PROJECT_ID \
--member=serviceAccount:$EXISTING_SERVICE_ACCOUNT \
--role=roles/artifactregistry.admin

gcloud projects add-iam-policy-binding $EXISTING_PROJECT_ID \
--member=serviceAccount:$EXISTING_SERVICE_ACCOUNT \
--role=roles/secretmanager.admin

gcloud projects add-iam-policy-binding $EXISTING_PROJECT_ID \
--member=serviceAccount:$EXISTING_SERVICE_ACCOUNT \
--role=roles/source.admin

gcloud projects add-iam-policy-binding $EXISTING_PROJECT_ID \
--member=serviceAccount:$EXISTING_SERVICE_ACCOUNT \
--role=roles/cloudbuild.builds.editor

gcloud projects add-iam-policy-binding $EXISTING_PROJECT_ID \
--member=serviceAccount:$EXISTING_SERVICE_ACCOUNT \
--role=roles/cloudscheduler.admin

gcloud projects add-iam-policy-binding $EXISTING_PROJECT_ID \
--member=serviceAccount:$EXISTING_SERVICE_ACCOUNT \
--role='roles/iam.serviceAccountUser'

gcloud projects add-iam-policy-binding $EXISTING_PROJECT_ID \
--member=serviceAccount:$EXISTING_SERVICE_ACCOUNT \
--role=roles/resourcemanager.projectIamAdmin

gcloud projects add-iam-policy-binding $EXISTING_PROJECT_ID \
--member=serviceAccount:$EXISTING_SERVICE_ACCOUNT \
--role=roles/iam.serviceAccountAdmin
```

### Grant User Rights to the Service Account

__Note:__ The user using this service account must have the necessary roles, `Service Account User` and `Service Account Token Creator`, to [impersonate](https://cloud.google.com/iam/docs/impersonating-service-accounts) the service account. 

```sh
gcloud iam service-accounts add-iam-policy-binding \
    $EXISTING_SERVICE_ACCOUNT \
    --member="user:$USER_ACCOUNT" \
    --role="roles/iam.serviceAccountUser" \
    --project=$EXISTING_SERVICE_ACCOUNT_PROJECT_ID


gcloud iam service-accounts add-iam-policy-binding \
    $EXISTING_SERVICE_ACCOUNT \
    --member="user:$USER_ACCOUNT" \
    --role="roles/iam.serviceAccountTokenCreator" \
    --project=$EXISTING_SERVICE_ACCOUNT_PROJECT_ID
```

## Create Infrastructure

With all set, now we are going to deploy the solution with terraform

### Change Backend tf State

Terraform doesn't allow Variables into the Backend configuration, because of this the bucket name should be changed directly in the backend.tf file, or simply initialize the backend with a parameter:

```sh
cd terraform
terraform init -backend-config="bucket=$TF_BUCKET_NAME"
```

<details>  
<summary><strong>OPTIONAL - </strong> If you would like to change the file, use the existing `TF_BUCKET_NAME` Variable:</summary>

```sh
cd terraform
sed -i 's/CHANGE_ME/'$TF_BUCKET_NAME'/g' backend.tf
```

</details>

## Deploy Infrastructure

There are two ways of deploying the resources. You will find them under `./terraform/executions`:

### Using a existing project

If you want to deploy the resources in an existing project you go to `./terraform/executions/clouddns-haa` folder and you will be executing the terraform  there.

### Creating a new project

If you want to deploy the resources, including the project you got to `./terraform/executions/clouddns-haa-standalone` folder and you will be executing the terraform there.

Prepare terraform by running terraform plan

```sh
terraform plan -out clouddns-sync.out
```

Deploy the infrastructure by running terraform apply

```sh
terraform apply clouddns-sync.out
```

Get from Terraform output the created project's ID and set an additional environment variable

```sh
export CDNS_PROJECT_ID=$(terraform output --raw output_project_id_dns)
```

Set the GCP project property in the gcloud config:

```bash
gcloud config set project $CDNS_PROJECT_ID
```

## Run the Synchronization Pipelines

Here we are going run the pipelines to sync the source DNS provider with Cloud DNS

### Permissions assigned for the user by Terraform

The following permissions were applied for the user in the new project in order to manage the new resources: 
- Cloud Build Editor
- Cloud Build Approver
- Source Repository Admin
- Secret Manager Admin
- Cloud DNS Admin

## Prepare the Cloud Build Pipelines

### Prepare Python Environment

**ATTENTION:** Check if the folder is either `../clouddns-haa/terraform/executions/clouddns-haa` or `../clouddns-haa/terraform/executions/clouddns-haa-standalone` before continuing...

```sh
cd ../../..
python3 -m venv env
source env/bin/activate
pip install -r build/requirements.txt
```

## Create Secrets and Pipeline files

Running the following python script, it will store the credentials in the secret manager, and create the pipeline files.

```bash
python3 main.py $SOURCE_PROVIDER
```

Add the generated files to git

```sh
git add *.json
git config user.email $USER_ACCOUNT
git config user.name "Your Name"
git commit -m "add pipelines files"
```

Push to the Google source repository

```sh
git push --all google
```

## Define a selected list of zones (**OPTIONAL**)

By default, all zones that your credentials have access to will be synchronized. You can specify which zones you want to synchronize by following the steps in this topic before running the python code.

Create a txt file named `zones.txt` in the root folder (clouddns-haa folder), specifying the zones you want to synchronize, following the pattern below (leading dot):

```terminal
#vi zones.txt
domain.com.us.
exampledomain.net. 
main.domain.com.us. 
```

After creating the txt file, just run the command below to store the zones in the secret manager:

```bash 
gcloud secrets create $(echo ${SOURCE_PROVIDER}_ZONES | tr '[:lower:]' '[:upper:]') --data-file=zones.txt --project=$CDNS_PROJECT_ID
```
Then just run the python file informing your source provider.

## Trigger the Pipelines

There are two triggers to interact with: **Plan** and **Apply**. There are 3 ways to execute the triggers: 
- Google Cloud Console
- Cloud Shell
- Webhook

In the next section, we provide the step-by-step to execute the **triggers**.

## Running Trigger in the Google Cloud Console

In the [Cloud Console](https://console.cloud.google.com/), select your **project**

### Plan
1. Go to the **Cloud Build** menu, click **Triggers**
1. Click **RUN** in the trigger with **plan** in its trigger name
1. Click **RUN TRIGGER**
1. Optionally, go to history menu and check the latest build to check the logs

### Apply

1. go to the **Cloud Build** menu, click **Triggers**
1. Click **RUN** in the trigger **apply** in its trigger name
1. Click **RUN TRIGGER**
1. Optionally, go to history menu and check the latest build to check the logs
<br/>

## Running Trigger from the Command Line

Please note that before running the commands below, it's important to make sure that the environment variables were exported in your shell at, in this case `$CDNS_PROJECT_ID` variable at the end of the Deploy Infrastructure step. Also you will call the trigger depending on what you have chosen: `manual` or `webook` triggers. 

### Plan

```sh
gcloud beta builds triggers run clouddns-haa-sync-plan --branch=main --project=$CDNS_PROJECT_ID
```

`OR`

```sh
gcloud beta builds triggers run clouddns-haa-webhook-plan --branch=main --project=$CDNS_PROJECT_ID
```


### Apply

```sh
gcloud beta builds triggers run clouddns-haa-sync-apply --branch=main --project=$CDNS_PROJECT_ID
```

`OR`

```sh
gcloud beta builds triggers run clouddns-haa-webhook-apply --branch=main --project=$CDNS_PROJECT_ID
```

## Run triggers via Webhook 

If the triggers were created with the webhook environment variable as true (TRIGGER_WEBHOOK) it's possible to invoke it using curl or any other external HTTP method, by making an HTTP request using the POST method. HTTP Post Request with Trigger Plan example: 

```terminal
curl -X POST \
        -H "application/json" \
        "https://cloudbuild.googleapis.com/v1/projects/$CDNS_PROJECT_ID/triggers/clouddns-haa-webhook-plan:webhook?key=API_KEY&secret=SECRET_VALUE" -d "{}"

```

The created triggers will have an URL as above example, only replacing the project id and the trigger id. Note that The API KEY and Secret Value will be automatically generated in the trigger creation. You can check the trigger URL via Console: 
1. Search for the Cloud build resource
1. Select Triggers
1. Select Global Region
1. Click on the trigger to check details 
1. Search for the Webhook URL Section 
1. Click URL Preview, the URL will be displayed, being able to copy it

With the URL copied it's possible to start running the triggers and check the process in the history menu, in Cloud Build Dashboard. 

## Next Steps

Up to now, this guide was to have everything ready to have your DNS zones hosted on Google Cloud DNS. Now, as mentioned in the beginning of the README, this solution is prepared for 3 use cases. 

In the following sections, there are some basic steps, outside the control of this solution that you will have to execute for each case.

### Migration Use Case

In case you are migrating to Cloud DNS, the recommended steps to follow to get the migration done are:
1. Reduce the TTL on your source provider (to 60 seconds)
1. Wait for about 48 hours to propagate
1. Rerun the trigger **Apply** to make sure everything is up-to-date
1. Go to your register and update each domain with the newly provided name servers on Google Cloud NDS

**OPTIONAL**: After a while, let's say, 2 weeks and everything is tested and running, you could change the TTL back to the original state.

### Active/Passive Use Case

For an Active/Passive mode, usually would be recommended to run the synchronization in a timely manner. For this, you would just enable the **Scheduler** feature of this solution. The time interval to be used will depends on how often you update your registers and how long it will take to synchronize. 

After the first synchronization, the synchronization runs reasonably fast, about 2-5 minutes, so if you change your records very often, setting the schudule for every 10 minutes would be feasible and will keep your registers safe on Cloud DNS. 
Please have a look at the NOTES.md where you can find some measured times of this process.

As it would work as a failover solution for your current provider, it is recommended to set the TTL for all zones to fastly refresh.

In case of disaster just go to your registrar and update each domain with the designated name servers on Google Cloud DNS for each zone.

### Active/Active Use Case

The Active/Active mode is a proposed Highly Available DNS Authority where you will be able to have 2 cloud providers working together in a way that if any cloud provider goes offline for any reason, the other will continue answering requests.

To configure this option, the **Scheduler** would also work, yet a more robust solution will be triggering the synchronization right after any change on your current provider. To do that, you would enable **Webhook** triggers and invoke this webhook from your current pipeline after a successful register update.

## Finish

You have deployed the solution and synchronized your current DNS provider with Cloud DNS

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>
