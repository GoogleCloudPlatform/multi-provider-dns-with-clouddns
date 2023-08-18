# Known Issues, Quotas and Limitations
At the investigation time, we discovered some restrictions related to the solution, and those are listed in this document.

## Common Errors 

### Already existing zone

If a zone that will be migrated from another provider already exists in another Cloud DNS project, the apply pipeline won't work, it'll be needed to remove from the source, or use the zones.txt to select all others, or to remove from the other project. 

OctoDNS and Google Cloud DNS will inform the user that they should confirm the domain ownership in order to continue. 

### Terraform and Billing Account
When running the terraform apply script, you can face the following error message:

  **Error message**: <br />
  
  ```terminal
  *module.project-factory.module.project-factory.google_project.main: Creating...*
  ...
  *Error: failed pre-requisites: failed to check permissions on billing account "billingAccounts/<BILLING_ACCOUNT_ID>": Post "https://cloudbilling.googleapis.com/v1/billingAccounts/<BILLING_ACCOUNT_ID>:testIamPermissions?alt=json&prettyPrint=false": impersonate: status code 403: {
     "error": {
       "code": 403,
       "message": "Permission 'iam.serviceAccounts.getAccessToken' denied on resource (or it may not exist).",
       "status": "PERMISSION_DENIED",
       "details": [{
           "@type": "type.googleapis.com/google.rpc.ErrorInfo",
           "reason": "IAM_PERMISSION_DENIED",
           "domain": "iam.googleapis.com",
           "metadata": {
             "permission": "iam.serviceAccounts.getAccessToken"
           }}]}}*

     *with module.project-factory.module.project-factory.google_project.main,
     on .terraform/modules/project-factory/modules/core_project_factory/main.tf line 73, in resource "google_project" "main":
     73: resource "google_project" "main" {*
  ```
  
  **Problem:**
  
  This can be related to the propagation of permissions, or the Terraform service account doesn't have permission to link new projects. 

  **Solution:**
  
  The solution for this is waiting a short time and run again the **terraform plan** / **terraform apply** commands. And check the Terraform Service Account permissions.

### Consumer Invalid - Python and Source Provider
When running the command to create the Secrets inside Google Cloud Secret Manager,
```
python3 main.py $SOURCE_PROVIDER 
```
User may face an error with the following message: 

```
[...] 
reason: "CONSUMER_INVALID"
domain: "googleapis.com"
metadata {
  key: "service"
  value: "secretmanager.googleapis.com"
}
metadata {
  key: "consumer"
  value: "projects/None"
}
]
```
**Solution**

The user must export the Cloud DNS project variable from terraform, and try again: 

```
cd terraform; export CDNS_PROJECT_ID=$(terraform \
    output --raw \
    output_project_id_dns)
```

### Permission Issues

Although we are using terraform to create the infrastructure, 2 permissions aren't being applied correctly.

**Problem**

When running the command (**terraform plan / terraform apply**) you will probably get a message that terraform created all resources. But, if you rerun the (**terraform plan**) command, you will notice that the following features need to be added again

```
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  ~ update in-place

Terraform will perform the following actions:

  # google_project_iam_binding.cb_sa["roles/dns.admin"] will be updated in-place
  ~ resource "google_project_iam_binding" "cb_sa" {
        id      = "<project-id>/roles/dns.admin"
      ~ members = [
          - "user:user@example.com",
            # (2 unchanged elements hidden)]
        # (3 unchanged attributes hidden)}

  # google_project_iam_binding.cb_sa["roles/secretmanager.secretAccessor"] will be updated in-place
  ~ resource "google_project_iam_binding" "cb_sa" {
        id      = "<project-id>/roles/secretmanager.secretAccessor"
      ~ members = [
          - "user:user@example.com",
            # (2 unchanged elements hidden)]
        # (3 unchanged attributes hidden)}

Plan: 0 to add, 2 to change, 0 to destroy.
```

**Temporary Solution**

The solution for this was to add manually (via Google Cloud Console) the permissions that wasn't applied via Terraform.
```
"roles/secretmanager.secretAccessor"
"roles/dns.admin"
```

## Limitations

### AWS Routing Policy

[OctoDNS](https://github.com/octodns), which is the software behind this solution, doesn't support the migration of the routing policies from AWS Route53 ([more information from the OctoDNS Provider](https://github.com/octodns/octodns-googlecloud/#support-information)) to Google Cloud DNS. Please also take a look at Cloud DNS [Supported DNS record types for Google Cloud DNS](https://cloud.google.com/dns/docs/records-overview). When trying to migrate, in the **Plan** or **Apply** cloud build trigger, OctoDNS will ignore the routing policies, and it'll migrate all (or selected) DNS Zones as a default routing policy. 

### Azure Traffic Manager

OctoDNS won't migrate the routing policies from Azure DNS as detailed on the [OCtoDNS Azure Provider](https://github.com/octodns/octodns-azure).

As addtional reference, In Azure, routing policies are managed differently from Google Cloud DNS. These are defined in the [Azure Traffic Manager](https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-routing-methods) resource. 

## Quotas

### AWS Quotas
AWS Route53 provide all informations about DNS Limits & Quotas, please consult this [link](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/DNSLimitations.html#limits-api-requests)

This section provide information about limits of **Route 53 API request**:

| Resource | Quota |
|----------|-------|
|Amazon Route 53 API requests | 5 requests per second per AWS account |

Review Quota data: Feb 3rd, 2023

### Azure Quotas

Azure DNS provide all informations about DNS Quotas, please consult this [link](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#azure-dns-limits)

### Google Cloud DNS Quotas

Cloud DNS provide all informations about DNS Quotas, please consult this [link](https://cloud.google.com/dns/quotas#resource_limits)

## Tips and Tricks 

### Re run build to pull new info

If the user already created all the infra, and already ran the plan and apply triggers, there's no need to run the cloud-build-img trigger every time. Each change on the Source provider, can be synced using the plan and apply triggers again. 
