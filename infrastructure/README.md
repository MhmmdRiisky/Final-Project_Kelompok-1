# Infrastructure Automation

This directory contains Ansible automation scripts for provisioning and configuring a containerized Kubernetes development environment on Azure VMs.

## Overview

This automation stack sets up a complete development environment with:
- **Docker** - Container runtime
- **Minikube** - Local Kubernetes cluster
- **Docker Registry** - Local container image registry

## Architecture

```
Azure VM (Ubuntu 22.04)
├── Docker Engine
├── Minikube Cluster
│   ├── kubectl (latest stable)
│   ├── Registry addon
│   └── Insecure registry configuration
└── Local Docker Registry (port 5000)
```

## Directory Structure

```
infrastructure/
├── ansible.cfg                 # Ansible configuration
├── inventories/
│   └── az-vm/
│       └── hosts.ini           # Target hosts inventory
├── playbooks/
│   └── site.yaml              # Main playbook
└── roles/
    ├── docker/                # Docker installation and configuration
    │   ├── files/
    │   │   └── daemon.json    # Docker daemon configuration
    │   └── tasks/
    │       └── main.yaml      # Docker installation tasks
    ├── minikube/              # Minikube setup
    │   └── tasks/
    │       └── main.yaml      # Minikube installation and configuration
    └── registry/              # Local Docker registry setup
        └── tasks/
            └── main.yaml      # Registry deployment tasks
```

## Components

### 1. Docker Role
- Installs Docker CE with all required dependencies
- Configures Docker daemon with insecure registry support
- Adds the target user to the docker group
- Enables and starts Docker service
- Verifies Docker installation and user access

**Key Features:**
- Automated GPG key and repository setup
- User permission configuration
- Service enablement and verification
- Insecure registry configuration for localhost:5000

### 2. Minikube Role
- Downloads and installs latest stable kubectl
- Downloads and installs latest Minikube
- Starts Minikube cluster with Docker driver
- Configures cluster with custom resource allocation
- Enables registry addon

**Configuration:**
- Driver: Docker
- CPUs: 2
- Memory: 2200MB
- Insecure registry: localhost:5000
- Profile: minikube

### 3. Registry Role
- Deploys local Docker registry container
- Creates persistent volume for registry data
- Configures port mapping (5000:5000)
- Sets up Minikube registry integration
- Creates registry aliases for seamless integration

**Registry Features:**
- Persistent storage with Docker volumes
- Always restart policy
- Port 5000 exposure
- Minikube registry addon integration

## Configuration

### Target Host Configuration
The inventory file (`inventories/az-vm/hosts.ini`) defines:
- **Target VM**: az-vm-01
- **IP Address**: 100.95.24.112
- **SSH User**: kel-1
- **SSH Key**: ~/.ssh/id_rsa

### Ansible Configuration
The `ansible.cfg` file configures:
- Default inventory path
- Disabled host key checking
- Disabled retry files
- Custom roles path

## Prerequisites

### Local Machine
- Ansible installed
- SSH access to target Azure VM
- Private SSH key configured

### Target Azure VM
- Ubuntu 22.04 LTS
- Sudo privileges for the specified user
- Internet connectivity
- Minimum 4GB RAM (recommended)
- Minimum 2 CPU cores

## Usage

### Running the Complete Setup
```bash
# From the infrastructure directory
ansible-playbook playbooks/site.yaml
```

### Running Individual Roles
```bash
# Docker only
ansible-playbook playbooks/site.yaml --tags docker

# Minikube only
ansible-playbook playbooks/site.yaml --tags minikube

# Registry only
ansible-playbook playbooks/site.yaml --tags registry
```

### Verifying the Installation
After successful deployment, verify the setup:

```bash
# SSH to the target VM
ssh -i ~/.ssh/id_rsa kel-1@100.95.24.112

# Check Docker
docker --version
docker ps

# Check Minikube
minikube status
kubectl get nodes

# Check Registry
curl http://localhost:5000/v2/_catalog
```

## Workflow

1. **Docker Installation**: Installs Docker CE, configures daemon, and sets up user permissions
2. **Minikube Setup**: Downloads kubectl and Minikube, starts cluster with Docker driver
3. **Registry Deployment**: Creates local registry container and configures Minikube integration

## Security Considerations

- Uses insecure registry configuration for localhost:5000
- SSH key-based authentication
- Host key checking disabled for automation
- Target user added to docker group for container access

## Troubleshooting

### Common Issues

**Docker Service Issues**:
- Check service status: `sudo systemctl status docker`
- Restart service: `sudo systemctl restart docker`

**Minikube Startup Issues**:
- Check driver: `minikube config get driver`
- Reset cluster: `minikube delete && minikube start`

**Registry Connection Issues**:
- Verify container: `docker ps | grep registry`
- Check port: `netstat -tlnp | grep 5000`

### Log Locations
- Docker logs: `journalctl -u docker`
- Minikube logs: `minikube logs`
- Registry logs: `docker logs registry`

## Maintenance

### Updates
- Regularly update Docker: Re-run docker role
- Update Minikube: Re-run minikube role
- Update kubectl: Automatically handled by minikube role

### Backup
- Registry data: Located in Docker volume `registry_data`
- Minikube config: `~/.minikube/` directory

## Technical Details

### Resource Allocation
- **Minikube**: 2 CPU cores, 2200MB RAM
- **Registry**: Default Docker resource limits
- **Total recommended**: 4GB RAM, 2+ CPU cores

### Network Configuration
- Registry: localhost:5000
- Minikube: Dynamic IP assignment
- kubectl: Communicates via Minikube context

### Storage
- Registry: Persistent Docker volume
- Minikube: VM-based storage
- Docker: Standard Docker root directory