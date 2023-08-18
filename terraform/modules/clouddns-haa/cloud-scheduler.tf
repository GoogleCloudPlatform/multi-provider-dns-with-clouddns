resource "google_cloud_scheduler_job" "sync-apply-job" {
  count                     = var.scheduler && !var.trigger_webhook ? 1 : 0
  project                   = var.project_id
  region                    = var.region
  name                      = "${var.prefix}-sync-apply-job"
  description               = "sync apply scheduled build trigger"
  schedule                  = var.scheduler_cron
  time_zone                 = var.scheduler_time_zone
  attempt_deadline          = "320s"

  http_target {
    http_method             = "POST"
    uri                     = "https://cloudbuild.googleapis.com/v1/projects/${var.project_id}/locations/global/triggers/${google_cloudbuild_trigger.manual-apply[0].trigger_id}:run"

    headers = {
      "User-Agent"          = "Google-Cloud-Scheduler"
    }
    oauth_token {
      service_account_email = google_service_account.cloud_scheduler.email
      scope                 = "https://www.googleapis.com/auth/cloud-platform"
    }
  }
}
