variable "environment" {
  type = string
  default = "dev"
}

variable "project" {
  default = "terraform-tests-301918"
}

variable "credentials_file" {
  default = "~/dev/terraform/tf-admin.json"
}

variable "region" {
  default = "us-central1"
}

variable "zone" {
  default = "us-central1-c"
}

variable "user" {
  default = "eduardo.laruta@gmail.com"
}

variable "service_name" {
  description = "Name for the cloud run service"
  default = "finance-tracker-service"
}

variable "github_account_name" {
  description = "Github account name"
  default = "tabris2015"
}

variable "github_repo_name" {
  description = "Name of github repo"
  default = "simple-finance-tracker"
}

locals {
  default_image = "us-docker.pkg.dev/cloudrun/container/hello"
  container_image = "gcr.io/${var.project}/${var.service_name}"
  digest = "latest"
}
