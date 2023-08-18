variable "project_id" {
  type        = string
  description = "Cloud DNS project which is created by terraform"
  default     = "prj-clouddns-sync"
}

variable "organization_id" {
  type        = string
  description = "Organization id for Cloud DNS project to be implemented"
  sensitive   = true
}

variable "folder_id" {
  type          = string
  description   = "Folder to setup projects - optional"
  default       = ""
  sensitive     = true
}

variable "billing_account" {
  type        = string
  description = "Billing Account id for Cloud DNS project to be implemented"
  sensitive   = true
}