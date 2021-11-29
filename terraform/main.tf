terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

# -------------------------------------------------------
# PROVIDER
# -------------------------------------------------------

provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project
  region      = var.region
  zone        = var.zone
}

provider "google-beta" {
  credentials = file(var.credentials_file)
  project     = var.project
  region      = var.region
  zone        = var.zone
}

# -------------------------------------------------------
# CLOUD RUN SERVICE
# -------------------------------------------------------

resource "google_cloud_run_service" "backend_service" {
  name     = var.service_name
  location = var.region

  template {
    spec {
      containers {
        image = "${local.default_image}:${local.digest}"
        resources {
          limits = {
            cpu    = "1.0"
            memory = "128Mi"
          }
        }
      }
    }
    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = "1"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_service.backend_service.location
  project     = google_cloud_run_service.backend_service.project
  service     = google_cloud_run_service.backend_service.name

  policy_data = data.google_iam_policy.noauth.policy_data
}

# -------------------------------------------
# CLOUD BUILD TRIGGER
# -------------------------------------------
resource "google_cloudbuild_trigger" "dev_backend_build_trigger" {
  provider = google-beta
  project = var.project
  name = "${var.service_name}-dev-build-trigger"
  description = "Cloud Build trigger for backend service in dev environment"

  github {
    owner = var.github_account_name
    name   = var.github_repo_name

    push {
      branch = "master"
    }
  }

  filename = "cloudbuild/dev.yaml"
  depends_on = [ google_cloud_run_service.backend_service ]
}


output "service_url"   {
  value = google_cloud_run_service.backend_service.status[0].url
}