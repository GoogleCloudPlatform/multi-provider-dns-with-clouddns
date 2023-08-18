locals {
    project_id = "prj-clouddns-sync"
}

module "clouddns-haa-base-project" {
    source = "../../modules/clouddns-haa-base-project"

    project_id = local.project_id
    organization_id = var.organization_id
    folder_id = var.folder_id
    billing_account = var.billing_account
}

module "clouddns-haa" {
    source = "../../modules/clouddns-haa"

    project_id             = module.clouddns-haa-base-project.output_project_id_dns
    project_number         = module.clouddns-haa-base-project.output_project_number_dns
    zone                   = var.zone
    region                 = var.region
    service_account        = var.service_account
    source_provider        = var.source_provider
    user_account           = var.user_account
    csrc_repo              = var.csrc_repo
    gar_repo               = var.gar_repo
    trigger_webhook        = var.trigger_webhook
    trigger_apply_approval = var.trigger_apply_approval
    trigger_plan_approval  = var.trigger_apply_approval
    scheduler              = var.scheduler
    scheduler_cron         = var.scheduler_cron
    scheduler_time_zone    = var.scheduler_time_zone
}
