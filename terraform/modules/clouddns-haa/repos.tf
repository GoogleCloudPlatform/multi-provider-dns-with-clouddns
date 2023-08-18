resource "google_sourcerepo_repository" "clouddns-repo" {
  project = var.project_id
  name    = var.csrc_repo
}

resource "null_resource" "push-csrc-repo" {
  provisioner "local-exec" {
    command = <<EOF
      cd ..
      git config credential.helper gcloud.sh
      git remote add google https://source.developers.google.com/p/${var.project_id}/r/${var.csrc_repo}
      git push --all google
      EOF
  }

  provisioner "local-exec" {
    when    = destroy
    command = <<EOF
      git remote remove google
      EOF
  }

  
  depends_on = [google_sourcerepo_repository.clouddns-repo]

}

resource "google_artifact_registry_repository" "artf_registry" {
  location      = var.region
  repository_id = var.gar_repo
  description   = "Docker Repository"
  format        = "DOCKER"
  project       = var.project_id
}
