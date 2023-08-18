# This file gets the Cloud build Service account
# then assigns the roles for it, such as secret manager viewer
# and DNS admin in order to cloud build be able to actually change the DNS 
resource "google_project_service_identity" "cb_sa" {
  provider = google-beta
  project = var.project_id
  service = "cloudbuild.googleapis.com"
}

resource "google_project_iam_member" "cb_sa" {
  project = var.project_id
  for_each = toset([
    "roles/secretmanager.secretAccessor",
    "roles/dns.admin",
    "roles/secretmanager.admin"    
  ])
  role    = each.key
  member  = "serviceAccount:${google_project_service_identity.cb_sa.email}"
}

resource "google_project_iam_member" "cb_sa_service" {
 project = var.project_id
  for_each = toset([
   "roles/secretmanager.admin"    
  ])
  role    = each.key
  member  = "serviceAccount:service-${var.project_number}@gcp-sa-cloudbuild.iam.gserviceaccount.com"
}
