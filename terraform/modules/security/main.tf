variable "project_name" {
  description = "Name prefix for project resources"
  type        = string
}

variable "vpc_id" {
  description = "VPC where the security group will be created"
  type        = string
}

variable "ssh_allowed_cidr" {
  description = "Trusted public IP CIDR allowed to SSH"
  type        = string
}

resource "aws_security_group" "app" {
  name        = "${var.project_name}-app-sg"
  description = "Security group for student platform application"
  vpc_id      = var.vpc_id

  ingress {
    description = "HTTP via Nginx"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH from trusted IP only"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }

  egress {
    description = "Allow outbound traffic for updates and image downloads"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "${var.project_name}-app-sg"
    Project = var.project_name
  }
}

output "security_group_id" {
  value = aws_security_group.app.id
}
