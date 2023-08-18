module "project-factory" {
  source            = "terraform-google-modules/project-factory/google"
  random_project_id = true
  name              = var.project_id
  project_id        = var.project_id
  org_id            = var.organization_id
  billing_account   = var.billing_account
  folder_id         = var.folder_id

  default_service_account = "deprivilege"
  auto_create_network     = false

  activate_apis = [
    "serviceusage.googleapis.com",
    "iam.googleapis.com",
    "dns.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com",
    "sourcerepo.googleapis.com",
    "secretmanager.googleapis.com",
    "cloudbilling.googleapis.com",
    "cloudscheduler.googleapis.com"
  ]
}
