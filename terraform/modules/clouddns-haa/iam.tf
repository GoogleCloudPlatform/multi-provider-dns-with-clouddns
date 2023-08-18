resource "google_project_iam_member" "user-account-iam" {
  project = var.project_id
  for_each = toset([
    "roles/cloudbuild.builds.editor",
    "roles/cloudbuild.builds.approver",
    "roles/cloudscheduler.jobRunner",
    "roles/source.admin",
    "roles/secretmanager.admin",
    "roles/dns.admin",
    "roles/logging.viewer",
    "roles/serviceusage.apiKeysAdmin",
    "roles/cloudscheduler.admin"
  ])
  role    = each.key
  member  = "user:${var.user_account}"
}

resource "google_service_account" "cloud_scheduler" {
  account_id        = "cloud-scheduler"
  display_name      = "⏱ cloud-scheduler"
  description       = "Service account for scheduling jobs on Cloud Scheduler"
  project           = var.project_id
}

resource "google_project_iam_member" "cloud_scheduler" {
  for_each = toset([
    "roles/appengine.appAdmin",
    "roles/appengine.appCreator",
    "roles/cloudscheduler.admin",
    "roles/cloudbuild.builds.builder",
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.cloud_scheduler.email}"
  depends_on = [
    google_service_account.cloud_scheduler
  ]
}
