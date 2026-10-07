terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Provision Amazon EKS Cluster for Control Tower Deployment
module "eks_cluster" {
  source       = "./modules/k8s_cluster"
  cluster_name = var.cluster_name
  environment  = var.environment
}

# Provision Elasticache Redis for Session Caching
module "storage" {
  source      = "./modules/storage"
  environment = var.environment
}