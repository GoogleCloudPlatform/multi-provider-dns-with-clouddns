module "clouddns-haa" {
    source = "../../modules/clouddns-haa"

    project_id             = var.existing_project_id
    project_number         = var.existing_project_number
    zone                   = var.zone
    region                 = var.region
    service_account        = var.existing_service_account
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