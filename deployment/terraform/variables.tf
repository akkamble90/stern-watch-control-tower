variable "aws_region" {
  description = "AWS Region for Infrastructure Provisioning"
  type        = string
  default     = "eu-central-1" # Frankfurt AWS Region for European Operations
}

variable "cluster_name" {
  description = "EKS Kubernetes Cluster Name"
  type        = string
  default     = "stern-watch-production-cluster"
}

variable "environment" {
  description = "Deployment Environment (prod/staging/dev)"
  type        = string
  default     = "production"
}