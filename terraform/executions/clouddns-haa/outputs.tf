output "output_project_id_dns" {
  value       = var.existing_project_id
  description = "The ID of the project of deployed resources"
}

output "output_cloudbuild_sa" {
  value       = module.clouddns-haa.output_cloudbuild_sa
  description = "The ID of Cloud Build Plan SA"
}
