variable "aws_region" {
  description = "AWS region for the deployment"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project resource name prefix"
  type        = string
  default     = "student-record-platform"
}

variable "vpc_cidr" {
  description = "VPC network CIDR"
  type        = string
  default     = "10.1.0.0/16"
}

variable "public_subnet_cidr" {
  description = "Public subnet CIDR"
  type        = string
  default     = "10.1.1.0/24"
}

variable "availability_zone" {
  description = "Availability zone for the subnet"
  type        = string
  default     = "ap-south-1a"
}

variable "ssh_allowed_cidr" {
  description = "Trusted public IPv4 CIDR allowed to connect over SSH"
  type        = string
}

variable "ami_id" {
  description = "Ubuntu 22.04 AMI ID in the selected region"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "Existing EC2 key pair name in AWS"
  type        = string
}
