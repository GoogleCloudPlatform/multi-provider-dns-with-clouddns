This document provides information about environment variables used by this Solution.

If you want to proceed with implementation in this README.md, get the information and use them with the root GUIDE.md .

## Variables to be used in Command Line

To deploy Cloud Build, you will need to work with enviroment variables, below has
some information about the type and description of these.

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| BILLING\_ACCOUNT | The ID of the billing account to associate projects with. | `string` | n/a | yes |
| BILLING\_ORG\_ID | The ID Billing Organization. Used when the billing to be used is linked to another organization. | `string` | n/a | yes |
| ORGANIZATION\_ID | The Organization ID to be used on implementation. | `string` | n/a | yes |
| FOLDER\_ID | Name prefix to use for folders created. Should be the same in all steps. | `string` | n/a | yes |
| REGION | Region will be defined to work on project | `string` | n/a | yes |
| ZONE | Zone will be defined to work on project | `string` | n/a | yes |
| USER\_ACCOUNT | You can get the user mail address to work on project | `string` | `$(gcloud config get-value account)` | yes |
| TF\_SA\_NAME | Name of the impersonated service account to deploy the resources. | `string` | `"sa-clouddns-tf"` | yes |
| BUCKET\_NAME | Name of the bucket to store the tf state. | `string` | n/a | yes |
| TF\_PROJECT\_ID | Project ID where service account and the bucket for for storing the tf state resides. | `string` | n/a | yes |
| SOURCE\_PROVIDER | External provider to pull DNS Zones, you can choose `"route53"` or `"azure"`. | `string` | n/a | yes |
| SCHEDULER | Scheduler you can create a period of time to execute the triggers using this method, for that it is necessary that the variable receive the value `"true"`, it is also necessary to insert the parameters for the variables SCHEDULER_TIME_ZONE and SCHEDULER_CRON. | `bool` | `false` | no |
| SCHEDULER\_TIME\_ZONE | Cloud Scheduler Time Zone variable. <br /> You can choose the time zone according to you local time zone, the values should be something like this `"America/New_York"`| `string` | `""` | no |
| SCHEDULER\_CRON | Cloud Scheduler Cron job, the value should be in this format `"* * * * *"`. You can see more about this in the official [Google-Documentation](https://cloud.google.com/scheduler/docs/configuring/cron-job-schedules?hl=pt-br#cron_job_format). | `string` | `""` | no |
| TRIGGER\_WEBHOOK | Webhook you can use this trigger activation method in Cloud Build via URL, for that it is necessary that this variable receive the value `"true"`. See the step-by-step of use in [Webhook](/GUIDE.md#run-triggers-via-webhook) | `bool` | `false` | no |
| TRIGGER\_PLAN\_APPROVAL | Auto approval on Cloud Build in Plan mode. | `bool` | `"false"` | yes |
| TRIGGER\_APPLY\_APPROVAL | Auto approval on Cloud Build in Apply mode. | `bool` | `"false"` | yes |

## Variable to be used in Terraform

The variables below will receive values from previously defined variables?

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| TF\_VAR\_billing\_account | This variable will inherit Billing Account variable value. | `string` | `$BILLING_ACCOUNT` | yes |
| TF\_VAR\_organization\_id | This variable will inherit Organization ID variable value. | `string` | `$ORGANIZATION_ID` | yes |
| TF\_VAR\_folder\_id | This variable will inherit Folder ID variable value. | `string` | `$FOLDER_ID` | yes |
| TF\_VAR\_region | This variable will inherit Region variable value. | `string` | `$REGION` | yes |
| TF\_VAR\_zone | This variable will inherit Zone variable value. | `string` | `$ZONE` | yes |
| TF\_VAR\_user\_account | This variable will inherit User Account variable value. | `string` | `$USER_ACCOUNT` | yes |
| TF\_VAR\_service\_account | This variable will inherit TF Service Account variable value. | `string` | `$TF_SA_NAME@$TF_PROJECT_ID.iam.gserviceaccount.com` | yes |
| TF\_VAR\_source\_provider | This variable will inherit Source Provider variable value. | `string` | `$SOURCE_PROVIDER` | yes |
| TF\_VAR\_scheduler | This variable will inherit Cloud Scheduler variable value. | `bool` | `$SCHEDULER` | no |
| TF\_VAR\_scheduler\_time\_zone | This variable will inherit Cloud Scheduler variable value. | `string` | `$SCHEDULER_TIME_ZONE` | no |
| TF\_VAR\_scheduler\_cron | This variable will inherit Cloud Scheduler variable value. | `string` | `$SCHEDULER_CRON` | no |
| TF\_VAR\_trigger\_webhook | This variable will inherit Cloud Scheduler variable value. | `bool` | `$TRIGGER_WEBHOOK` | no |
| TF\_VAR\_plan\_approval | This variable will inherit Plan Approval variable value. | `bool` | `$TRIGGER_PLAN_APPROVAL` | yes |
| TF\_VAR\_apply\_approval | This variable will inherit Apply Approval variable value. | `bool` | `$TRIGGER_APPLY_APPROVAL` | yes |
