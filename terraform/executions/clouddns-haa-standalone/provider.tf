provider "google" {
  impersonate_service_account = var.service_account
}

provider "google-beta" {
  impersonate_service_account = var.service_account
}
