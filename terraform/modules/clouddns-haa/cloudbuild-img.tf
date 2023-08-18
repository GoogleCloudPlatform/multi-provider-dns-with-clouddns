resource "google_cloudbuild_trigger" "clouddns-build-img" {
  location = "global"
  name     = "${var.prefix}-build-img"
  project  = var.project_id

  source_to_build {
    uri       = "https://source.developers.google.com/p/${var.project_id}/r/${var.csrc_repo}"
    ref       = "refs/heads/main"
    repo_type = "CLOUD_SOURCE_REPOSITORIES"
  }

  build {
    images = ["${var.region}-docker.pkg.dev/${var.project_id}/${var.gar_repo}/clouddns-haa:latest"]

    step {
      name = "gcr.io/cloud-builders/docker"
      dir  = "build"
      args = ["build", "-t", "${var.region}-docker.pkg.dev/${var.project_id}/${var.gar_repo}/clouddns-haa:latest", "-f", "Dockerfile", "."]
    }

  }

  depends_on=[null_resource.push-csrc-repo]

}

module "gcloud" {
  source  = "terraform-google-modules/gcloud/google"
  version = "~> 2.0"

  platform = "linux"
  additional_components = ["alpha"]

  create_cmd_entrypoint  = "gcloud"
  create_cmd_body        = "alpha builds triggers run ${google_cloudbuild_trigger.clouddns-build-img.name} --branch=main --project=${var.project_id}"
  module_depends_on = ["google_cloudbuild_trigger.clouddns-build-img", "null_resource.push-csrc-repo"]
}
