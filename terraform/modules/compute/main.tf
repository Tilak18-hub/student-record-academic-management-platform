variable "project_name" {
  description = "Name prefix for project resources"
  type        = string
}

variable "ami_id" {
  description = "Ubuntu 22.04 AMI ID for the selected AWS region"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "subnet_id" {
  description = "Public subnet ID"
  type        = string
}

variable "security_group_id" {
  description = "Application security group ID"
  type        = string
}

variable "key_name" {
  description = "Existing EC2 key pair name"
  type        = string
}

resource "aws_instance" "app" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [var.security_group_id]
  key_name                    = var.key_name
  associate_public_ip_address = true

  user_data = <<-USERDATA
    #!/bin/bash
    set -eux

    apt-get update
    DEBIAN_FRONTEND=noninteractive apt-get install -y docker.io nginx
    systemctl enable --now docker
    systemctl enable --now nginx

    cat > /etc/nginx/sites-available/student-record-platform <<'NGINX'
    server {
        listen 80 default_server;
        listen [::]:80 default_server;
        server_name _;

        location / {
            proxy_pass http://127.0.0.1:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    NGINX

    rm -f /etc/nginx/sites-enabled/default
    ln -sfn /etc/nginx/sites-available/student-record-platform /etc/nginx/sites-enabled/student-record-platform
    nginx -t
    systemctl reload nginx
  USERDATA

  root_block_device {
    volume_size = 12
    volume_type = "gp3"
    encrypted   = true
  }

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  tags = {
    Name    = "${var.project_name}-app-server"
    Project = var.project_name
    Role    = "application"
  }
}

output "instance_id" {
  value = aws_instance.app.id
}

output "public_ip" {
  value = aws_instance.app.public_ip
}
