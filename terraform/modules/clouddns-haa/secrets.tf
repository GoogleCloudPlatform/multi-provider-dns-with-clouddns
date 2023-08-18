resource "random_password" "secret" {
  count     = var.trigger_webhook ? 1 : 0
  length    = 16
  special   = true
}

resource "google_secret_manager_secret" "webhook" {
  count     = var.trigger_webhook ? 1 : 0
  project   =  var.project_id
  secret_id = "WEBHOOK"

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "trigger_webhook_secret_key_data" {
  count     = var.trigger_webhook ? 1 : 0
  secret    = google_secret_manager_secret.webhook[0].id

  secret_data = random_password.secret[0].result
}
