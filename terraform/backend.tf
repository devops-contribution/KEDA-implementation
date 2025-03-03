terraform {
  backend "s3" {
    bucket         = "kind-cluster-remote-backend-bucket"
    key            = "kind-cluster/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "kind-cluster-terraform-locks"
  }
}