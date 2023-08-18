output "output_cloudbuild_sa" {
  value       = google_project_service_identity.cb_sa.email
  description = "The ID of Cloud Build Plan SA"
}

