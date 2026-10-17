# 🎓 Student Record & Academic Management Platform

<p align="center">
  <strong>A Cloud-Native DevOps Project Built with AWS, Terraform, Ansible, Docker, Flask and Nginx</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AWS-Cloud%20Infrastructure-orange?logo=amazonaws" alt="AWS"/>
  <img src="https://img.shields.io/badge/Terraform-Infrastructure%20as%20Code-7B42BC?logo=terraform" alt="Terraform"/>
  <img src="https://img.shields.io/badge/Ansible-Automation-EE0000?logo=ansible" alt="Ansible"/>
  <img src="https://img.shields.io/badge/Docker-Containerization-2496ED?logo=docker" alt="Docker"/>
  <img src="https://img.shields.io/badge/Python-Flask-3776AB?logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/Deployment-Success-brightgreen" alt="Deployment"/>
</p>

## 📌 Project Overview

The **Student Record & Academic Management Platform** is a web-based application designed to manage student information, course details, and academic marks through a dashboard and REST API.

The project demonstrates how modern DevOps practices can automate cloud infrastructure provisioning, server configuration, containerized application deployment, and application verification.

AWS resources are provisioned using Terraform, Ansible automates application deployment, Docker packages the Flask application, and Nginx serves public HTTP traffic as a reverse proxy.

## 🎯 Project Objectives

- Implement Infrastructure as Code using Terraform.
- Provision a VPC, public subnet, routing, security group, and EC2 instance.
- Automate server configuration and deployment with Ansible.
- Containerize a Python Flask application using Docker.
- Configure Nginx as a reverse proxy.
- Build REST APIs for student and academic marks management.
- Persist application data using a Docker volume and SQLite.
- Verify deployment through automated tests and live API requests.
- Maintain source code and deployment configuration in GitHub.

## ✨ Key Features

- **Student Management:** Create and retrieve student records.
- **Course Information:** Store each student's course details.
- **Academic Marks:** Record marks for individual students and subjects.
- **Data Relationships:** Associate academic results with registered students.
- **REST API:** Access application functionality through HTTP endpoints.
- **Web Dashboard:** Provide a browser-based interface for student and marks management.
- **Containerization:** Package the application into a Docker image.
- **Persistent Storage:** Store SQLite data in a Docker-managed volume.
- **Automated Provisioning:** Create AWS infrastructure using Terraform.
- **Configuration Management:** Deploy the application using Ansible.
- **Reverse Proxy:** Route HTTP requests through Nginx.
- **Automated Testing:** Validate application behavior using Pytest.

## 🏗️ System Architecture

```text
                     Developer / Controller EC2
                               |
                +--------------+--------------+
                |                             |
                v                             v
             Terraform                      Ansible
                |                             |
                v                             v
         AWS Infrastructure          Application EC2 Server
                |                             |
                |                    +--------+--------+
                |                    |                 |
                v                    v                 v
           AWS VPC               Nginx :80          Docker
                |                    |                 |
          Public Subnet               |                 v
                |                    +----------> Flask App
          Internet Gateway                         :8080
                |                                      |
          Route Table                                 v
                |                                SQLite Database
          Security Group                            Docker Volume
                |
          EC2 Application Server
```

### Request Flow

1. A user opens the application using the EC2 public IP.
2. The AWS security group permits HTTP traffic on port 80.
3. Nginx receives the request and forwards it to `127.0.0.1:8080`.
4. The Flask application processes the request.
5. The application reads or updates SQLite records.
6. The API response is returned to the client through Nginx.

### Infrastructure Automation Flow

1. Terraform provisions the AWS networking and compute resources.
2. The EC2 startup script installs Docker and Nginx.
3. Ansible connects to the application server over SSH.
4. Ansible transfers the application files and builds the Docker image.
5. Ansible starts the container, creates persistent storage, and configures Nginx.
6. Ansible verifies the application health endpoint.

## 🛠️ Technology Stack

| Technology | Role |
|---|---|
| AWS EC2 | Cloud compute for the application |
| AWS VPC | Isolated virtual network |
| AWS Subnet | Application network placement |
| Internet Gateway | Internet connectivity for the public subnet |
| Security Groups | Network access control |
| Terraform | Infrastructure as Code |
| Ansible | Configuration management and deployment |
| Docker | Application containerization |
| Nginx | HTTP reverse proxy |
| Python | Application programming language |
| Flask | Web framework and REST API |
| SQLite | Relational data storage |
| Gunicorn | Python WSGI application server |
| Pytest | Automated application tests |
| Git | Source control |
| GitHub | Remote repository and collaboration |

## ☁️ AWS Infrastructure

The application was deployed in the AWS Mumbai region.

| Resource | Configuration |
|---|---|
| AWS Region | `ap-south-1` |
| EC2 instance type | `t3.micro` |
| VPC CIDR | `10.1.0.0/16` |
| Public subnet CIDR | `10.1.1.0/24` |
| HTTP port | `80` |
| SSH port | `22`, restricted to a trusted IP |
| Application port | `8080`, bound to localhost |
| Root EBS volume | 12 GB, encrypted |
| Metadata service | IMDSv2 required |

The actual instance type, account eligibility, and AWS charges depend on the AWS account and region. Free-tier eligibility is not a guarantee of zero cost.

### Terraform-Managed Resources

- Virtual Private Cloud (VPC)
- Public subnet
- Internet gateway
- Public route table
- Route table association
- Application security group
- EC2 application instance

Terraform outputs provide the instance ID, public IP, VPC ID, subnet ID, and application URL.

## 🌐 Live Application

The application was verified at the following endpoints:

| Endpoint | Purpose |
|---|---|
| [Web Dashboard](http://52.66.214.43/) | Open the student management interface |
| [Health API](http://52.66.214.43/api/health) | Check application health |
| [Students API](http://52.66.214.43/api/students) | Retrieve student records |
| [Marks API](http://52.66.214.43/api/marks) | Retrieve academic marks |

**Deployment note:** The public IP can change if the EC2 instance is replaced or its public address changes. These links use HTTP and are intended for demonstration only.

## 🔌 REST API Documentation

### 1. Application Health

**Method:** `GET`

**Endpoint:** `/api/health`

Example:

```bash
curl http://52.66.214.43/api/health
```

Example response:

```json
{
  "service": "student-record-platform",
  "status": "healthy"
}
```

### 2. Retrieve Students

**Method:** `GET`

**Endpoint:** `/api/students`

```bash
curl http://52.66.214.43/api/students
```

Returns the registered student records.

### 3. Create a Student

**Method:** `POST`

**Endpoint:** `/api/students`

```bash
curl -X POST http://52.66.214.43/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aarav Sharma",
    "email": "aarav.test@example.com",
    "course": "Computer Science"
  }'
```

Expected HTTP status: `201 Created`.

Example response:

```json
{
  "course": "Computer Science",
  "email": "aarav.test@example.com",
  "id": 1,
  "name": "Aarav Sharma"
}
```

The API validates student information and prevents duplicate email registrations.

### 4. Retrieve Academic Marks

**Method:** `GET`

**Endpoint:** `/api/marks`

```bash
curl http://52.66.214.43/api/marks
```

Returns academic marks with the associated student information.

### 5. Record Academic Marks

**Method:** `POST`

**Endpoint:** `/api/marks`

```bash
curl -X POST http://52.66.214.43/api/marks \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "subject": "Cloud Computing",
    "score": 92
  }'
```

Expected HTTP status: `201 Created`.

Example response:

```json
{
  "id": 1,
  "score": 92.0,
  "student_id": 1,
  "subject": "Cloud Computing"
}
```

The score must be between 0 and 100, and the referenced student must exist.

## 📁 Repository Structure

```text
student-record-academic-management-platform/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       └── js/
├── tests/
│   └── test_app.py
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tfvars
│   └── modules/
│       ├── network/
│       ├── security/
│       └── compute/
├── ansible/
│   ├── inventory.ini
│   └── site.yml
├── docs/
│   └── screenshots/
├── Dockerfile
├── requirements.txt
├── wsgi.py
├── .gitignore
└── README.md
```

Terraform state, local variables, plan files, and credentials must remain excluded from Git even if they exist in the local working directory.

## 🚀 Getting Started

### Prerequisites

Install or configure:

- Python 3 and pip
- Docker
- Terraform
- Ansible
- AWS CLI
- An AWS account with the required permissions
- SSH access to the target EC2 instance

Use an attached IAM role or another approved AWS credential mechanism. Do not hard-code credentials into source files.

### Run Locally

Clone the repository:

```bash
git clone https://github.com/Tilak18-hub/student-record-academic-management-platform.git
cd student-record-academic-management-platform
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
gunicorn --bind 127.0.0.1:8080 wsgi:app
```

Open:

`http://127.0.0.1:8080/`

### Run Automated Tests

```bash
python -m pytest -q
```

The test suite previously passed five tests. Rerun the command to verify the current source revision.

### Build the Docker Image

```bash
docker build -t student-record-platform:1.0 .
```

### Provision AWS Infrastructure

Initialize Terraform:

```bash
terraform -chdir=terraform init
```

Validate the configuration:

```bash
terraform -chdir=terraform validate
```

Review the planned changes:

```bash
terraform -chdir=terraform plan
```

Apply only after reviewing the plan:

```bash
terraform -chdir=terraform apply
```

View the outputs:

```bash
terraform -chdir=terraform output
```

**Important:** Terraform may create billable AWS resources. Review the instance type, region, storage, and cost implications before applying.

### Configure and Deploy with Ansible

Update `ansible/inventory.ini` with the correct target IP and private-key path.

Install the Docker collection:

```bash
ansible-galaxy collection install community.docker
```

Test connectivity:

```bash
ansible -i ansible/inventory.ini student_app -m ping
```

Deploy:

```bash
ansible-playbook -i ansible/inventory.ini ansible/site.yml
```

Verify the deployment:

```bash
curl http://YOUR_EC2_PUBLIC_IP/api/health
```

Replace `YOUR_EC2_PUBLIC_IP` with the current public IP of the application server.

## ✅ Testing and Deployment Results

The following results were observed during the project deployment:

| Verification | Result |
|---|---|
| Terraform validation | Passed |
| Terraform infrastructure provisioning | Successful |
| SSH connection to application EC2 | Successful |
| Docker service | Active |
| Nginx service | Active |
| Ansible deployment | Successful |
| Ansible failed tasks | 0 |
| Application health endpoint | Healthy |
| Student creation API | HTTP 201 |
| Academic marks API | HTTP 201 |
| Student retrieval API | Verified |
| Marks retrieval API | Verified |
| Application data relationship | Verified |

Ansible reported 14 successful task results, 5 changed tasks, zero failures, and zero unreachable hosts in the recorded deployment.

## 🔐 Security and Best Practices

- Restrict SSH access to trusted source IP addresses.
- Do not expose the internal application port 8080 publicly.
- Use Nginx as the public HTTP entry point.
- Keep private keys, GitHub tokens, credentials, `.env` files, and secret variable files out of Git.
- Never commit Terraform state files or saved plans.
- Review security-group rules and IAM permissions using least privilege.
- Enable HTTPS before using the application for real users.
- Add authentication, authorization, audit logging, backups, and appropriate privacy controls before handling real student data.
- Use synthetic data in public demonstrations.
- Treat a successful deployment as a technical milestone, not as a production security certification.

## 🧹 Resource Cleanup

To inspect the resources Terraform would destroy:

```bash
terraform -chdir=terraform plan -destroy
```

When you are ready to remove the project's AWS infrastructure:

```bash
terraform -chdir=terraform destroy
```

Review the proposed destruction and confirm only when you intend to delete these resources. Back up any required database information first. Check the AWS console afterward for any remaining resources that Terraform does not manage.

## 👨‍💻 Author

**Student:** Tilak Bhutada

**GitHub:** [Tilak18-hub](https://github.com/Tilak18-hub)

**Project Repository:** [Student Record & Academic Management Platform](https://github.com/Tilak18-hub/student-record-academic-management-platform)

---

<p align="center">
  <strong>Built as a hands-on DevOps project to practice cloud infrastructure, automation, containers, and application deployment.</strong>
</p>
