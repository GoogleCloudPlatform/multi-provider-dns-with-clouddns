This document provides information about environment variables used by this Solution.

If you want to proceed with implementation in this README.md, get the information and use them with the root GUIDE.md .

## Variables to be used in Command Line

To deploy Cloud Build, you will need to work with enviroment variables, below has
some information about the type and description of these.

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| REGION | Region will be defined to work on project. | `string` | n/a | yes |
| ZONE | Zone will be defined to work on project. | `string` | n/a | yes |
| USER\_ACCOUNT | You can get the user mail address to work on project. | `string` | `$(gcloud config get-value account)` | yes |
| SOURCE\_PROVIDER | External provider to pull DNS Zones, you can choose `"route53"` or `"azure"`. | `string` | n/a | yes |
| SCHEDULER | Scheduler you can create a period of time to execute the triggers using this method, for that it is necessary that the variable receive the value `"true"`, it is also necessary to insert the parameters for the variables SCHEDULER_TIME_ZONE and SCHEDULER_CRON. | `bool` | `false` | no |
| SCHEDULER\_TIME\_ZONE | Cloud Scheduler Time Zone variable. <br /> You can choose the time zone according to you local time zone, the values should be something like this `"America/New_York"`| `string` | `""` | no |
| SCHEDULER\_CRON | Cloud Scheduler Cron job, the value should be in this format `"* * * * *"`. You can see more about this in the official [Google-Documentation](https://cloud.google.com/scheduler/docs/configuring/cron-job-schedules?hl=pt-br#cron_job_format). | `string` | `""` | no |
| TRIGGER\_WEBHOOK | Webhook you can use this trigger activation method in Cloud Build via URL, for that it is necessary that this variable receive the value `"true"`. See the step-by-step of use in [Webhook](/GUIDE.md#run-triggers-via-webhook) | `bool` | `false` | no |
| TRIGGER\_PLAN\_APPROVAL | Auto approval on Cloud Build in Plan mode. | `bool` | `"false"` | yes |
| TRIGGER\_APPLY\_APPROVAL | Auto approval on Cloud Build in Apply mode. | `bool` | `"false"` | yes |
| EXISTING\_PROJECT\_ID | Existing project id where you will deploy the solution resources. | `string` | n/a | yes |
| EXISTING\_PROJECT\_NUMBER | Existing project number where you will deploy the solution resources. | `string` | n/a | yes |

## Variable to be used in Terraform

The variables below will receive values from previously defined variables?

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| TF\_VAR\_project\_id | This variable will be automatically generated or inherit Existing Project ID variable. | `string` | `$EXISTING_PROJECT_ID` or `auto generated` | yes |
| TF\_VAR\_project\_number | This variable will be automatically generated or inherit Existing Project Number variable. | `string` | `$EXISTING_PROJECT_NUMBER` or `auto generated` | yes |
| TF\_VAR\_source\_provider | This variable will inherit Source Provider variable value. | `string` | `$SOURCE_PROVIDER` | yes |
| TF\_VAR\_region | This variable will inherit Region variable value. | `string` | `$REGION` | yes |
| TF\_VAR\_zone | This variable will inherit Zone variable value. | `string` | `$ZONE` | yes |
| TF\_VAR\_user\_account | This variable will inherit User Account variable value. | `string` | `$USER_ACCOUNT` | yes |
| TF\_VAR\_trigger\_webhook | This variable will inherit Cloud Scheduler variable value. | `bool` | `$TRIGGER_WEBHOOK` | no |
| TF\_VAR\_scheduler | This variable will inherit Cloud Scheduler variable value. | `bool` | `$SCHEDULER` | no |
| TF\_VAR\_scheduler\_time\_zone | This variable will inherit Cloud Scheduler variable value. | `string` | `$SCHEDULER_TIME_ZONE` | no |
| TF\_VAR\_scheduler\_cron | This variable will inherit Cloud Scheduler variable value. | `string` | `$SCHEDULER_CRON` | no |
| TF\_VAR\_plan\_approval | This variable will inherit Plan Approval variable value. | `bool` | `$TRIGGER_PLAN_APPROVAL` | yes |
| TF\_VAR\_apply\_approval | This variable will inherit Apply Approval variable value. | `bool` | `$TRIGGER_APPLY_APPROVAL` | yes |

