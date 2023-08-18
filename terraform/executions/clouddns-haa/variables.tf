variable "existing_project_id" {
  type        = string
  description = "Cloud DNS project used to deploy the resources"
}

variable "existing_project_number" {
  type        = string
  description = "Cloud DNS project number used to deploy the resources"
}

variable "existing_service_account" {
  type        = string
  description = "Service account for terraform to implement resources"
}

variable "zone" {
  type = string
  description = "default zone"
}

variable "region" {
  type        = string
  description = "Default region"
}

variable "source_provider" {
  type          = string
  description   = "External provider to pull DNS Zones"
}

variable "user_account" {
  type = string
  description = "User Account Variable "
}

variable "csrc_repo" {
  type          = string
  description   = "Cloud source repository name"
  default       = "clouddns-haa-repo" 
}

variable "gar_repo" {
  type = string
  description = "Artifact Registry repository"
  default = "clouddns-haa-artifact-repo"
}

variable "trigger_plan_approval" {
  type          = bool
  description   = "Variable to define need for approval of cloud build plan trigger"
  default       = false
}

variable "trigger_apply_approval" {
  type          = bool
  description   = "Variable to define need for approval of cloud build apply trigger"
  default       = false
}

variable "trigger_webhook" {
  type          = bool
  description   = "Variable to use a webhook type trigger and not a manual trigger"
  default       = false 
}

variable "scheduler" {
  type          = bool
  description   = "Variable to enable Cloud Scheduler feature"
  default       = false
}

variable "scheduler_time_zone" {
  type          = string
  description   = "Specifies the time zone to be used in interpreting schedule"
  default       = ""
}

variable "scheduler_cron" {
  type          = string
  description   = "Describes the schedule on which the job will be executed"
  default       = ""
}
