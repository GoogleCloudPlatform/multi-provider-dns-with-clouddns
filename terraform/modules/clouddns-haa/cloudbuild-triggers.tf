resource "google_cloudbuild_trigger" "manual-plan" {
  count    = var.trigger_webhook ? 0 : 1
  location = "global"
  name     = "${var.prefix}-sync-plan"
  project  = var.project_id
  
  source_to_build {
    uri       = "https://source.developers.google.com/p/${var.project_id}/r/${var.csrc_repo}"
    ref       = "refs/heads/main"
    repo_type = "CLOUD_SOURCE_REPOSITORIES"
  }

  substitutions = {
    _PROVIDER       = var.source_provider
    _GAR_REGION     = var.region
    _GAR_REPOSITORY = var.gar_repo
  }

  filename = "${var.prefix}-plan.json"

  approval_config {
    approval_required = var.trigger_plan_approval
  }

  depends_on=[null_resource.push-csrc-repo]

}

resource "google_cloudbuild_trigger" "manual-apply" {
  count    = var.trigger_webhook ? 0 : 1
  location = "global"
  name     = "${var.prefix}-sync-apply"
  project  = var.project_id
  
  source_to_build {
    uri       = "https://source.developers.google.com/p/${var.project_id}/r/${var.csrc_repo}"
    ref       = "refs/heads/main"
    repo_type = "CLOUD_SOURCE_REPOSITORIES"
  }

  substitutions = {
    _PROVIDER       = var.source_provider
    _GAR_REGION     = var.region
    _GAR_REPOSITORY = var.gar_repo
  }

  filename = "${var.prefix}-apply.json"

  approval_config {
    approval_required = var.trigger_apply_approval
  }

  depends_on=[null_resource.push-csrc-repo]

}

resource "google_cloudbuild_trigger" "webhook-plan" {
  count    = var.trigger_webhook ? 1 : 0
  location = "global"
  name     = "${var.prefix}-webhook-plan"
  project  = var.project_id

 webhook_config {
    secret = google_secret_manager_secret_version.trigger_webhook_secret_key_data[0].id
  }

  source_to_build {
    uri       = "https://source.developers.google.com/p/${var.project_id}/r/${var.csrc_repo}"
    ref       = "refs/heads/main"
    repo_type = "CLOUD_SOURCE_REPOSITORIES"
  }

  git_file_source {
    path      = "${var.prefix}-plan.json"
    uri       = "https://source.developers.google.com/p/${var.project_id}/r/${var.csrc_repo}"
    revision  = "refs/heads/main"
    repo_type = "CLOUD_SOURCE_REPOSITORIES"
  }

  substitutions = {
    _PROVIDER       = var.source_provider
    _GAR_REGION     = var.region
    _GAR_REPOSITORY = var.gar_repo
  }
}

resource "google_cloudbuild_trigger" "webhook-apply" {
  count    = var.trigger_webhook ? 1 : 0
  location = "global"
  name     = "${var.prefix}-webhook-apply"
  project  = var.project_id

 webhook_config {
    secret = google_secret_manager_secret_version.trigger_webhook_secret_key_data[0].id
  }

  source_to_build {
    uri       = "https://source.developers.google.com/p/${var.project_id}/r/${var.csrc_repo}"
    ref       = "refs/heads/main"
    repo_type = "CLOUD_SOURCE_REPOSITORIES"
  }

  git_file_source {
    path      = "${var.prefix}-apply.json"
    uri       = "https://source.developers.google.com/p/${var.project_id}/r/${var.csrc_repo}"
    revision  = "refs/heads/main"
    repo_type = "CLOUD_SOURCE_REPOSITORIES"
  }

  substitutions = {
    _PROVIDER       = var.source_provider
    _GAR_REGION     = var.region
    _GAR_REPOSITORY = var.gar_repo
  }
}
