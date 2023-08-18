output "output_project_id_dns" {
  value       = module.clouddns-haa-base-project.output_project_id_dns
  description = "The ID of the created project"
}

output "output_cloudbuild_sa" {
  value       = module.clouddns-haa.output_cloudbuild_sa
  description = "The ID of Cloud Build Plan SA"
}
