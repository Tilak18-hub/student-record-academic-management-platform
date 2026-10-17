output "vpc_id" {
  description = "ID of the project VPC"
  value       = module.network.vpc_id
}

output "public_subnet_id" {
  description = "ID of the public subnet"
  value       = module.network.public_subnet_id
}

output "app_instance_id" {
  description = "ID of the application EC2 instance"
  value       = module.compute.instance_id
}

output "app_public_ip" {
  description = "Public IPv4 address of the application server"
  value       = module.compute.public_ip
}

output "app_url" {
  description = "Public URL of the application"
  value       = "http://${module.compute.public_ip}"
}
