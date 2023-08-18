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
| ORGANIZATION\_ID | The Organization ID to be used on implementation. | `string` | n/a | yes |
| FOLDER\_ID | Name prefix to use for folders created. Should be the same in all steps. | `string` | n/a | yes |

## Variable to be used in Terraform

The variables below will receive values from previously defined variables?

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| TF\_VAR\_billing\_account | This variable will inherit Billing Account variable value. | `string` | `$BILLING_ACCOUNT` | yes |
| TF\_VAR\_organization\_id | This variable will inherit Organization ID variable value. | `string` | `$ORGANIZATION_ID` | yes |
| TF\_VAR\_folder\_id | This variable will inherit Folder ID variable value. | `string` | `$FOLDER_ID` | yes |

